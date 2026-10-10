# Source terms review — Phase 2

Review date: 2026-10-10  
Purpose: decide whether publicly indexed interview-experience pages can be treated as an automatically usable corpus for Prepline.

## Findings from the current published terms

- **LeetCode:** https://leetcode.com/terms/ states that crawling, scraping, and spidering any part of the service are prohibited, and its content section describes platform content as copyrighted/proprietary unless otherwise specified.
- **GeeksforGeeks:** https://www.geeksforgeeks.org/legal/terms-of-use/ prohibits systematically retrieving data/content to create or compile a collection, compilation, database, or directory without written permission. It also prohibits data mining/robots and unauthorized automated extraction.
- **GeeksforGeeks copyright information:** https://www.geeksforgeeks.org/legal/copyright-information/ says unauthorized transmission, publication, or use of site content without prior knowledge or written permission is prohibited.

## Decision for this repository

**Permission is not established.** Public visibility is not equivalent to permission to collect and redistribute the content. The existing interview rows and 202 mapping candidates contain short factual topic summaries and source URLs; they must remain review candidates and must not be represented as a legally cleared production dataset.

Do not run automated scraping against these services. Before using their material as the Phase 2/Phase 13 corpus, obtain written permission or replace those records with data whose license clearly permits the intended collection, storage, transformation, and evaluation.

## What is still required

1. Obtain written permission from the relevant source owner(s), or replace the source corpus with appropriately licensed / directly contributed reports.
2. Review at least 15 distinct eligible reports, verify role/cohort fit, and record report-level deduplication evidence.
3. Record the actual permission basis, reviewer, and review date in the source review ledger.
4. Only then consider rows for the production dataset. Do not infer legal approval from a public URL, search snippet, or this summary.

This is a source-terms risk review, not legal advice or a legal opinion.
