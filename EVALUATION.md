# EvidenceDesk evaluation

## Automated checks

17 tests pass locally on Windows with Python 3.14.
The GitHub Actions workflow also passes on Ubuntu with Python 3.14.

Tests cover chunking, cosine similarity, retrieval orchestration,
and rejection of selected invalid inputs. External API calls are mocked.

## Manual checks

Document: Road_Rules_Good_Citizen.pdf
Prepared collection: 3 pages, 18 chunks.

| Check | Observed result |
|---|---|
| Accident question | Retrieved the accident section and generated an answer with source labels |
| Pedestrian question | Generated an answer with inspectable source passages |
| Monthly insurance cost | Acknowledged insufficient evidence instead of supplying a price |
| PDF upload and preparation | Produced 18 chunks |
| Evidence display | Showed passage text, filename, page, and chunk |
| Remove uploaded PDF | Cleared the active document, answer, and evidence from the interface |

## Limitations

These are development spot checks, not a comprehensive benchmark.
No aggregate accuracy, hallucination rate, or retrieval-recall claim
has been established. Citation support still requires review.