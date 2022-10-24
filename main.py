#!/usr/bin/env python3
import arrow as arrow

import jira
import util
from util import input_bool

if __name__ == '__main__':
    j = jira.Jira()
    useLastSprint = input_bool("Use last Sprint? [y/N] ")
    isSecondSprintWeek = input_bool("Is this the second Spint Week? [y/N] ")
    startOffset = 0
    startOffset -= useLastSprint * 2
    startOffset -= isSecondSprintWeek
    endOffset = -isSecondSprintWeek
    TIMEFRAME_START = arrow.now().shift(weeks=startOffset).floor('week') \
        if useLastSprint else arrow.now().shift(weeks=startOffset).floor('week')
    TIMEFRAME_END = arrow.now().shift(weeks=endOffset).floor('week') if useLastSprint else arrow.now()

    print(f"Getting data from {TIMEFRAME_START.humanize()} until {TIMEFRAME_END.humanize()}")

    jql = f"worklogDate >= startOfWeek({startOffset}) AND worklogDate < startOfWeek({endOffset if endOffset != 0 else ''}) AND worklogAuthor = currentUser()"\
        if useLastSprint else f"worklogDate > startOfWeek({endOffset if endOffset != 0 else ''}) AND worklogAuthor = currentUser()"
    issues = j.get_issues(jql)
    j.attach_worklogs(issues, TIMEFRAME_START, TIMEFRAME_END)

    printTemplate = "{:>8} | {:<30} | {:^8} | {:>10}"
    total_work_logged = 0
    print()
    print(printTemplate.format("Issue", "Summary", "Status", "Time spent"))
    for issue in issues:
        secondsSpent = issue['timeSpentSeconds']
        total_work_logged += secondsSpent
        print(printTemplate.format(issue['key'], issue['summary'][:30], issue['status'],
                                   util.format_time(secondsSpent)))
    print()
    print(f"Total Time Spent:{util.format_time(total_work_logged)} or{util.format_time(total_work_logged, True)}")
