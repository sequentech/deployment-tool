## 103111.9 (24/11/2017)

* Fix some deployment issues on agora-dev-box
* Remove difference between real and test elections
* Open onboarding whenever the user has no elections created
* Duplicated elections didn't preserve question options urls, fixed
* Hide features link on top navbar on admin login/signup
* Enable deregistration for admin users
* Hide input element on tlf/email census config on gui-admin

## 103111.8 (6/11/2017)

* Enable start_date and end_date to be null (upon election creation), correctly update user's last_login field
* On gui-admin, when user clicks on add question, the question now has two voting options included by default
* Save drafts of elections

## 103111.7 (23/10/2017)

* Fix problems with resend code button. Add resend option for email. Add allow_user_resend option to allow users to get codes even on closed census elections
* Add version number to config.yml on agora-dev-box and check it on config_prod_env helper script
* Fix onboarding error that broke the logic of the app, and didn't show the profile when it's empty. Improve admin fields errors
* Make profile left column wider
* Code refactor to fix problem when trying to add CSV text to election census on an election that hasn't been created yet
* Fix erroneous candidate when clicking on new question while creating an election
* Add option to authapi to signal that a registration failed because the user already exists

## 103111.6 (06/10/2017)

* Use new settings widget on all the easy places on gui-admin
* Set abstract settings widgets to collapsed by default
* Add as global variables election and isDemo on booth to be used by external scripts
* Fix uncommented comment on dev-box helper script
* Use intl-tel-input library for phone logins
* Fix problem with int params on admin interface
* Some countries (Colombia, India) can't receive sms with alphanumeric senders, use phone number instead
* Don't collapse most admin settings, show collapse/expand sign on hover
* While creating an election on gui-admin, don't allow to add the auth method as an extra field, as it generated problems
* Redirect default route to admin login
* Added Onboarding Tour when the user first logins

## 103111.5 (20/09/2017)

* Add twilio backend for SMS messages
* Fix html question descriptions on gui-elections
* Set upsert defaults to an empty string on agora-dev-box
* Improve repmgr deployment on agora-dev-box
* Solve encoding checking issue in booth
* Check if admin profile needs to be reopened when it's closed
* Add a template election parameter to dev-box to make it easily configurable
* Add default name to extra fields, fixing undefined name issue while creating the election
* Simplify footer: powered by and social links
* Enable using profile variables on new election template
* Fix script to copy config from one env to another
* Fix logo css on gui-admin
* Fix some public urls

## 103111.4 (17-09-2017)

* Make configurable at deployment which layouts and electoral systems are available as options in the administrative interface
* Add configurable help menu list
* fix configurable signup link on gui-admin
* Add admin profile modal, and a header menu to access it
* Fix slave deployment connection with master, related to postgres backup configuration
* Solve a number of small issues with agora-dev-box deployment
* Add script to  export configuration from staging environment to production env

## 103111.3 (14-08-2017)

- Fixed issue on gui-admin with int fields
- Fixed issue with parameters of error strings on gui-admin
- Improve logging on authmethods
- Use new settings interface on 'Basic details' on gui-admin
- Add auth messages for admins as config params on agora-dev-box

## 103111.2 (27-07-2017)

- Define admin-fields to agora-dev-box.
- Fixes to postgres backups.
- Add always_publish parameter to agora-dev-box.
- Enable multiple logins at once on the same browser.
- Add check for encoding overflow on gui-booth
- Configure auth msg defaults from agora-dev-box's config.yml

## 103111.1 (30-06-2017)

- Add desborda2 voting system.
- Warn about void values on import tsv on agora-tools.
- Fix java 7 use on agora-verifier.
- Add support for SMS OTP method for admins.
- Add SaaS features.

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