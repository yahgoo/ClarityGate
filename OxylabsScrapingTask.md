Role: Objective
You are an expert data engineer working in Qoder Expert Mode, using the Oxylabs
Web Scraper API/MCP integration to gather scraping test cases and deny-list
fields for the WorkBuddy Grill Mode distillation pipeline.

Tech Stack
- Python 3.11
- Oxylabs Web Scraper API (credentials in .env as OXYLABS_USERNAME / OXYLABS_PASSWORD)
- Output format: JSON + Markdown summary

Critical Rules / Constraints
1. Work iteratively — implement ONE script/task at a time, test before moving to the next.
2. Do not modify any existing ClarityGate or WorkBuddy source files, prompts, or
   coach definitions. This is a standalone, isolated task.
3. Autonomous execution — self-debug errors and retry without stopping for manual input.
4. Respect target site terms of service and robots.txt for every scrape target.
5. Save all raw scraped output and a deduplicated, cleaned summary — do not
   discard intermediate data.
6. Use Qwen3-Max-Preview for this Expert Mode session (off-peak discount window).

Project Structure
output/
  oxylabs_raw/          <- raw scrape results per target, one JSON file each
  oxylabs_deny_list.md  <- expanded deny-list fields, deduplicated
  oxylabs_test_cases.md <- 5-10 new distillation test cases derived from scraped examples
  oxylabs_run_summary.md <- what was scraped, from where, counts, and any errors

Immediate Task — Oxylabs Scraping for Deny-List + Test-Case Expansion

1. Confirm Oxylabs credentials are present and the connection works with a
   single test request before running the full task. Report the test result.

2. Scrape
 1. https://github.com/search?q=is%3Aissue+%22feature+request%22&type=issues
 2. https://www.producthunt.com/
 3. https://www.reddit.com/r/agile/ (or r/ProductManagement)
 4. https://stackoverflow.com/questions/tagged/requirements
 for real-world examples of vague, ambiguous,
   or poorly-specified requirement text.

3. From the scraped content, extract:
   - New candidate deny-list terms/fields (words/phrases that should be flagged
     as vague, e.g. "fast", "user-friendly", "seamlessly") — append to
     output/oxylabs_deny_list.md, deduplicated against any existing deny-list.
   - 5-10 new compact distillation test cases (short requirement snippets, 1-3
     sentences each) that could be run through the 5 Grill Mode coaches later.
     Save to output/oxylabs_test_cases.md in the same format as the existing
     test case file [reference existing test case file if available].

4. Produce output/oxylabs_run_summary.md summarizing: targets scraped, number
   of raw items collected, number of deny-list terms added, number of test
   cases generated, and any scrape failures/errors encountered.

5. Do not run these new test cases through the Grill Mode coaches yet — that
   is a separate task for tomorrow's saturation review. This task only
   produces the raw material.

Report back with: connection test result, scrape counts per target, and a
preview of 3 sample test cases before finalizing all files.