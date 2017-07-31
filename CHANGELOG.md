## 103111.3 (??-??-2017)

- Fix issue on gui-admin with int fields
- Fixed issue with parameters of error strings on gui-admin

## 103111.2 (27-07-2017)

- define admin-fields to agora-dev-box.
- fixes to postgres backups.
- add always_publish parameter to agora-dev-box.
- enable multiple logins at once on the same browser.
- add check for encoding overflow on gui-booth

## 103111.1 (30-06-2017)

- add desborda2 voting system.
- warn about void values on import tsv on agora-tools.
- fix java 7 use on agora-verifier.
- add support for SMS OTP method for admins.
- add SaaS features.

## 17.04 (29-04-2017)

- Add desborda voting system.
- Enable selection by category with one click.
- Enable drag n drop on mobile platforms.
- Improve language configuration on ansible deployments.
- Make dumpvotes faster (hours down to seconds).
- Add tool to generate votes for benchmarking.
- Improve permissions granularity: create-real-elections.
- Add callback from agora_elections to auth system to enable limiting revotes.
- Automate creating zip for verifiable results.
- Add voted/not voted filter category to gui-admin to enable sending messages to those who haven't voted yet.
- Add script to populate config with random passwords.
- Improve postgres backups.
- Add PDF output to results formats.

## 3.4.0 (01-12-2016)
- Add support for multiple authentication methods per election.
- Enable editing the election json before creating the election.
- Add share buttons (Facebook, Twitter etc) to voting booth and public election site.
- Change gui colors to neutral ones.
- Improve encrypting screen in voting booth.
- Fix go.nvotes.com still links to old documentation
- Fix problem with logo/ng-src.
- Fix csv dump in agora-payments.
- Fix agora-elections admin config to enhance support for big elections.
- Fix problem that prevented admin login in certain cases.
- Fix census search.
- Make tally verifications easier.
- Enable shuffling specific categories.
- Show points for each voting option.
- Update themes.
- Limit the number of questions per election from config file.
- Upgrade to Postgres 9.4.
- Enable pre-registration.
- Use numeric and hyphen-separated authentication codes.
- Add confirm audit dialog on booth.
- Add confirm tally dialog on admin and enable tallying only active users.
- Add more granularity to authapi perms.
- Allow showing documentation after casting a vote.
- add support for filling the email/sms template with any variable from census data.
- Allow sending messages to voters at any step of the election process.
- Enable controlling the maximum number of allowed revotes.

## 3.3.0 (26-07-2016)

- Add description to simultaneous questions layout
- Enhance the legal page on the voting booth and election public site  and make them configurable.
- Add support for custom html in the admin console, elections gui and voting booth.
- Add copyright headers to most files on all Agora Voting projects.
- Refactor footer and include the footer on voting booth and the election public site.
- Fix next button while creating election on admin gui when success action is hidden.
- Fix reset tally command (used rarely, when all authorities agree to do a second tally) on election orchestra.
- Security improvement: verify client CAs for keydone/tallydone post messages to agora_elections.
- Fix eotest so that HTTPS is required and certificates and used and checked.
- Fix election orchestra so that HTTP connections are rejected.
- fix selfsigned CAs so that they work also when an external domain is configured.