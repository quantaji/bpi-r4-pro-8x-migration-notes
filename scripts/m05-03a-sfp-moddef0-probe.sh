#!/bin/sh
# Temporary M05.03a probe for the WAN SFP2 MOD_DEF0 input.

set -eu

DEBUG_GPIO=/sys/kernel/debug/gpio
INTERVAL_MS=100
COUNT=0
GPIO_NUM=
MODDEF0_OFFSET=1
CHANSEL_OFFSET=3
SFP_CHANNEL=1

usage() {
	cat <<'EOF'
Usage:
  m05-03a-sfp-moddef0-probe.sh [options]

Options:
  -c COUNT       Number of samples to read. Default: run until interrupted.
  -i MS          Sampling interval in milliseconds. Default: 100.
  -g GPIO        Debugfs global GPIO number for SFP2 MOD_DEF0.
  -o OFFSET      SoC GPIO offset for SFP2 MOD_DEF0. Default: 1.
  -m OFFSET      SoC GPIO offset for WAN mux select. Default: 3.
  -s CHANNEL     SFP-present channel used by 806 mux logic. Default: 1.
  -h             Show this help.

The script reads debugfs GPIO state and interprets MOD_DEF0 as GPIO_ACTIVE_LOW,
matching the 8X DTS and the value 806-02 receives through gpiod.
EOF
}

die() {
	echo "error: $*" >&2
	exit 1
}

mount_debugfs() {
	[ -r "$DEBUG_GPIO" ] && return 0

	mkdir -p /sys/kernel/debug 2>/dev/null || true
	mount -t debugfs none /sys/kernel/debug 2>/dev/null || true

	[ -r "$DEBUG_GPIO" ] || die "cannot read $DEBUG_GPIO; run as root and enable/mount debugfs"
}

gpio_from_line() {
	sed -n 's/.*gpio-\([0-9][0-9]*\).*/\1/p' | head -n 1
}

find_labeled_gpio() {
	awk '
		/gpio-[0-9]/ {
			line = tolower($0)
			if (line ~ /sfp2/ && line ~ /mod[-_ ]?def0/) {
				print $0
				exit
			}
		}
	' "$DEBUG_GPIO" | gpio_from_line
}

gpio_from_offset_with_filter() {
	offset="$1"
	filter="$2"

	awk -v off="$offset" -v filter="$filter" '
		/^gpiochip[0-9]+: GPIOs / {
			line = $0
			lower = tolower(line)
			if (filter != "" && lower !~ filter)
				next

			sub(/^.*GPIOs /, "", line)
			sub(/,.*/, "", line)
			split(line, r, "-")
			base = r[1] + 0
			end = r[2] + 0
			if (end >= base + off) {
				print base + off
				exit
			}
		}
	' "$DEBUG_GPIO"
}

gpio_from_offset() {
	offset="$1"
	gpio="$(gpio_from_offset_with_filter "$offset" "pinctrl|mediatek")"
	[ -n "$gpio" ] || gpio="$(gpio_from_offset_with_filter "$offset" "")"
	printf '%s\n' "$gpio"
}

read_gpio_line() {
	gpio="$1"
	grep -E "^[[:space:]]*gpio-$gpio([[:space:]]|$)" "$DEBUG_GPIO" | head -n 1
}

raw_from_line() {
	line="$1"
	case " $line " in
		*" hi "*)
			printf '1\n'
			;;
		*" lo "*)
			printf '0\n'
			;;
		*)
			printf 'unknown\n'
			;;
	esac
}

sleep_ms() {
	ms="$1"
	if command -v usleep >/dev/null 2>&1; then
		usleep "$((ms * 1000))"
	else
		sleep "$(awk -v ms="$ms" 'BEGIN { printf "%.3f", ms / 1000 }')"
	fi
}

print_header() {
	echo "moddef0_gpio=$GPIO_NUM moddef0_offset=$MODDEF0_OFFSET chansel_offset=$CHANSEL_OFFSET sfp_channel=$SFP_CHANNEL interval_ms=$INTERVAL_MS"
	echo "seq time raw_moddef0 sfp_present new_channel raw_chansel transition"
}

poll_loop() {
	chansel_gpio="$(gpio_from_offset "$CHANSEL_OFFSET")"
	seq=0
	prev_present=

	print_header

	while :; do
		line="$(read_gpio_line "$GPIO_NUM" || true)"
		[ -n "$line" ] || die "gpio-$GPIO_NUM is not visible in $DEBUG_GPIO"

		raw="$(raw_from_line "$line")"
		[ "$raw" != "unknown" ] || die "cannot parse GPIO value from: $line"

		if [ "$raw" -eq 0 ]; then
			present=1
		else
			present=0
		fi

		if [ "$present" -eq 1 ]; then
			new_channel="$SFP_CHANNEL"
		else
			new_channel=$((1 - SFP_CHANNEL))
		fi

		transition="-"
		if [ -n "$prev_present" ] && [ "$prev_present" != "$present" ]; then
			transition="present:$prev_present->$present"
		fi
		prev_present="$present"

		chansel_raw="-"
		if [ -n "$chansel_gpio" ]; then
			chansel_line="$(read_gpio_line "$chansel_gpio" || true)"
			[ -z "$chansel_line" ] || chansel_raw="$(raw_from_line "$chansel_line")"
		fi

		printf '%s %s %s %s %s %s %s\n' \
			"$seq" "$(date +%s)" "$raw" "$present" "$new_channel" \
			"$chansel_raw" "$transition"

		seq=$((seq + 1))
		if [ "$COUNT" -gt 0 ] && [ "$seq" -ge "$COUNT" ]; then
			break
		fi

		sleep_ms "$INTERVAL_MS"
	done
}

while getopts "c:i:g:o:m:s:h" opt; do
	case "$opt" in
		c)
			COUNT="$OPTARG"
			;;
		i)
			INTERVAL_MS="$OPTARG"
			;;
		g)
			GPIO_NUM="$OPTARG"
			;;
		o)
			MODDEF0_OFFSET="$OPTARG"
			;;
		m)
			CHANSEL_OFFSET="$OPTARG"
			;;
		s)
			SFP_CHANNEL="$OPTARG"
			;;
		h)
			usage
			exit 0
			;;
		*)
			usage >&2
			exit 2
			;;
	esac
done

case "$COUNT:$INTERVAL_MS:$MODDEF0_OFFSET:$CHANSEL_OFFSET:$SFP_CHANNEL" in
	*[!0-9:]*)
		die "COUNT, interval, offsets, and channel must be numeric"
		;;
esac

[ "$SFP_CHANNEL" -eq 0 ] || [ "$SFP_CHANNEL" -eq 1 ] || die "SFP channel must be 0 or 1"

mount_debugfs

if [ -z "$GPIO_NUM" ]; then
	GPIO_NUM="$(find_labeled_gpio)"
	[ -n "$GPIO_NUM" ] || GPIO_NUM="$(gpio_from_offset "$MODDEF0_OFFSET")"
fi

[ -n "$GPIO_NUM" ] || die "cannot locate MOD_DEF0 GPIO; pass the debugfs gpio number with -g"

poll_loop
