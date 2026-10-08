# crypto-lab-reddit-research

Read-only Reddit sentiment and attention collector for a personal, non-commercial cryptocurrency paper-trading research project.

## Purpose
The project reads public cryptocurrency discussions and produces aggregated signals such as asset mention counts, discussion activity, and changes in community attention. These signals are compared with external cryptocurrency market data in a paper-trading experiment using virtual funds only.

## Reddit usage
The collector is read-only. It does not post, comment, vote, send messages, moderate communities, or identify/profile individual Reddit users. Example public communities include r/CryptoCurrency, r/Bitcoin, r/ethereum, and r/solana.

## Privacy and credentials
Research output is aggregated at asset level. API credentials are supplied through environment variables and are never committed to this repository.

## Status
Research prototype. Reddit API access is subject to Reddit approval, and authentication may be adjusted to match the access method granted by Reddit.
