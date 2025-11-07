# [StructuredTool(name='add_time', description='Adds or subtracts a duration from a given time.', args_schema={'properties': {'duration': {'description': 'The duration to add or subtract. Use a negative value to subtract.\nExamples:\n- "1h2m3s" to add 1 hour,
#                 2 minutes, and 3 seconds.\n- "-1h" to subtract 1 hour.', 'type': 'string'
#             }, 'format': {'default': '2006-01-02T15: 04: 05Z07: 00', 'description': "Output time format. See the 'current_time' tool for detailed format options.", 'type': 'string'
#             }, 'time': {'description': 'Time in any format. Defaults to the current time.', 'type': 'string'
#             }, 'timezone': {'default': 'UTC', 'description': "The target timezone for the output, in IANA format (e.g., 'America/New_York').", 'type': 'string'
#             }
#         }, 'required': ['duration'
#         ], 'type': 'object'
#     }, metadata={'title': None, 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False
#     }, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x1072cbf60>), StructuredTool(name='compare_time', description='Compares two times. Returns -1 if the first time is before the second,
#     0 if they are equal, and 1 if the first time is after the second.', args_schema={'properties': {'time_a': {'description': 'The first time to compare.', 'type': 'string'
#             }, 'time_a_timezone': {'default': 'UTC', 'description': "Timezone form time_a, in IANA format (e.g., 'America/New_York').", 'type': 'string'
#             }, 'time_b': {'description': 'The second time to compare.', 'type': 'string'
#             }, 'time_b_timezone': {'default': 'UTC', 'description': "Timezone for time_b, in IANA format (e.g., 'America/New_York').", 'type': 'string'
#             }
#         }, 'required': ['time_a', 'time_b'
#         ], 'type': 'object'
#     }, metadata={'title': None, 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False
#     }, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x1072cbc40>), StructuredTool(name='convert_timezone', description='Converts a time from one timezone to another.', args_schema={'properties': {'format': {'default': '2006-01-02T15: 04: 05Z07: 00', 'description': "Output time format. See the 'current_time' tool for detailed format options.", 'type': 'string'
#             }, 'input_timezone': {'default': 'UTC', 'description': "The timezone of the input time, in IANA format (e.g., 'America/New_York'). If the input time string contains a timezone, it will take precedence.", 'type': 'string'
#             }, 'output_timezone': {'default': 'UTC', 'description': "The target timezone for the output, in IANA format (e.g., 'America/New_York').", 'type': 'string'
#             }, 'time': {'description': 'Time in any format. Defaults to the current time.', 'type': 'string'
#             }
#         }, 'type': 'object'
#     }, metadata={'title': None, 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False
#     }, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x1072cbd80>), StructuredTool(name='current_time', description='Returns the current time.', args_schema={'properties': {'format': {'default': '2006-01-02T15: 04: 05Z07: 00', 'description': 'The output time format, which can be a predefined format or a custom layout.\n\n## Predefined Formats\n\n`RFC850`, `RFC3339`, `Stamp`, `StampMicro`, `StampNano`, `Rubydate`, `RFC822z`, `DateTime`, `RFC1123z`, `RFC3339nano`, `StampMilli`, `TimeOnly`, `ANSIC`, `Unixdate`, `RFC822`, `RFC1123`, `Kitchen`, `DateOnly`\n\n## Custom Format\n\nA custom format can be built using the following components. Each component shows an example of how a part of the reference time is formatted. Only these values are recognized. Any text in the layout string that is not a recognized component will be treated as a literal.\n\n- Year: "2006",
#                 "06"\n- Month: "Jan",
#                 "January",
#                 "01",
#                 "1"\n- Day of the week: "Mon",
#                 "Monday"\n- Day of the month: "2",
#                 "_2",
#                 "02"\n- Day of the year: "__2",
#                 "002"\n- Hour: "15",
#                 "3",
#                 "03" (PM or AM)\n- Minute: "4",
#                 "04"\n- Second: "5",
#                 "05"\n- AM/PM mark: "PM"\n\n### Numeric Time Zone Offsets\n\n- "-0700"     (±hhmm)\n- "-07:00"    (±hh:mm)\n- "-07"       (±hh)\n- "-070000"   (±hhmmss)\n- "-07:00:00" (±hh:mm:ss)\n\nReplacing the sign with a "Z" triggers ISO 8601 behavior, which prints "Z" for the UTC zone:\n\n- "Z0700"      (Z or ±hhmm)\n- "Z07:00"     (Z or ±hh:mm)\n- "Z07"        (Z or ±hh)\n- "Z070000"    (Z or ±hhmmss)\n- "Z07:00:00"  (Z or ±hh:mm:ss)\n\nWithin the format string, the underscores in "_2" and "__2" represent spaces that may be replaced by digits if the following number has multiple digits, for compatibility with fixed-width Unix time formats. A leading zero represents a zero-padded value.\nThe formats __2 and 002 are space-padded and zero-padded three-character day of year; there is no unpadded day of year format.\n\n### Fractional Seconds\n\nA comma or decimal point followed by one or more zeros represents a fractional second, printed to the given number of decimal places. A comma or decimal point followed by one or more nines represents a fractional second with trailing zeros removed.\nFor example,
#                 "15:04:05.000" formats or parses with millisecond precision.', 'type': 'string'
#             }, 'timezone': {'default': 'UTC', 'description': "The target timezone for the output, in IANA format (e.g., 'America/New_York').", 'type': 'string'
#             }
#         }, 'type': 'object'
#     }, metadata={'title': None, 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False
#     }, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x10743a480>), StructuredTool(name='relative_time', description='Returns a time based on a relative natural language expression.', args_schema={'properties': {'format': {'default': '2006-01-02T15: 04: 05Z07: 00', 'description': "Output time format. See the 'current_time' tool for detailed format options.", 'type': 'string'
#             }, 'text': {'description': 'A relative time expression in natural language.\nExamples:\n- "now"\n- "today"\n- "yesterday"\n- "5 minutes ago"\n- "three days ago"\n- "last month"\n- "next month"\n- "one year from now"\n- "yesterday at 10am"\n- "last sunday at 5:30pm"\n- "sunday at 22:45"\n- "next January"\n- "last February"\n- "December 25th at 7:30am"\n- "10am"\n- "10:05pm"\n- "10:05:22pm"', 'type': 'string'
#             }, 'time': {'description': 'Time in any format. Defaults to the current time.', 'type': 'string'
#             }, 'timezone': {'default': 'UTC', 'description': "The target timezone for the output, in IANA format (e.g., 'America/New_York').", 'type': 'string'
#             }
#         }, 'required': ['text'
#         ], 'type': 'object'
#     }, metadata={'title': None, 'readOnlyHint': True, 'destructiveHint': False, 'idempotentHint': True, 'openWorldHint': False
#     }, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x10743a0c0>)
# ]
