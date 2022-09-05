/**
 * This file is part of deployment-tool.
 * Copyright (C) 2014-2016  Sequent Tech Inc <legal@sequentech.io>

 * deployment-tool is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License.

 * deployment-tool is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.

 * You should have received a copy of the GNU Affero General Public License
 * along with deployment-tool.  If not, see <http://www.gnu.org/licenses/>.
**/

/*
 * ConfigService is a function that returns the configuration that exists
 * in this same file, which you might want to edit and tune if needed.
 */

var SEQUENT_CONFIG_VERSION = '7.0.0-beta.1';

var SequentConfigData = {
  // the base url path for ajax requests, for example for sending ballots or
  // getting info about an election. This url is usually in the form of
  // 'https://foo/api/v3/' and always ends in '/'.
  base: '',
  theme: "{{ config.sequent_ui.theme }}",
  baseUrl: "https://{{config.ballot_box.domain}}/elections/api/",
  freeAuthId: 1,

  // Configurable Sign Up link
  signupLink: "{{ config.sequent_ui.organization.admin_signup_link }}",
  
  // Webpage title
  webTitle: "{{ config.sequent_ui.web_title }}",
  
  // html to be inserted in the gui-admin profile view
  profileHtml: "{{ config.sequent_ui.profile_html | regex_replace("\n", "") }}",
  
  // base url used for help on gui-admin
  settingsHelpBaseUrl: "{{ config.sequent_ui.settings_help_base_url }}",

  // default url used for help on gui-admin
  settingsHelpDefaultUrl: "{{ config.sequent_ui.settings_help_default_url }}",

  // html/text to show when the help url for a setting fails to load
  settingsHelpUrlError: "{{ config.sequent_ui.texts.settings_help_url_error | regex_replace("\n", "") }}",
  
  // Show 'Success Action' tab in admin sequent_ui
  showSuccessAction: {% if config.sequent_ui.show_success_action %}true{% else %}false{% endif %},

  // AuthApi base url
  authAPI: "https://{{config.ballot_box.domain}}/iam/api/",
  dnieUrl: "https://{{config.ballot_box.domain}}/iam/api/authmethod/dnie/auth/",
  // Agora Elections base url
  electionsAPI: "https://{{config.ballot_box.domain}}/elections/api/",

  // Agora Admin help url
  helpUrl: "{{ config.sequent_ui.technology.documentation }}",

  authorities: {{ config.auths }},
  director: "{{ config.director }}",

  // For admins:
  // Allow editing the election.presentation.theme_css so that any election
  // Admin can highly customize the election directly with CSS.
  // Allowed values: true|false
  allowCustomElectionThemeCss: {% if config.sequent_ui.allow_custom_election_theme_css %}true{% else %}false{% endif %},

  // For admins:
  // Allow editing the json description of the election before creating it
  // Allowed values: true|false
  allowEditElectionJson: {% if config.sequent_ui.allow_edit_election_json %}true{% else %}false{% endif %},

  // Allow admin users registration
  // Allowed values: true|false
  allowAdminRegistration: {% if config.iam.allow_admin_registration %}true{% else %}false{% endif %},

  // show the documentation links after successfully casting a vote
  // allowed values: true| false
  showDocOnVoteCast: {% if config.sequent_ui.show_doc_on_vote_cast %}true{% else %}false{% endif %},

  // if true, the calculated results are always automatically published
  // valid values: true, false
  always_publish: {% if config.ballot_box.always_publish %}true{% else %}false{% endif %},

  calculateResultsDefault: {{ config.sequent_ui.calculate_results_default }},

  // default template election for gui-admin
  electionTemplate: "{{ config.sequent_ui.election_template | regex_replace('\n', '') }}",

  // help links list
  // html code for flexibility
  helpList: [
    {% for help_item in config.sequent_ui.help_list %}
    "{{ help_item | regex_replace('\n', '') }}"{% if not loop.last %},{% endif %}
    {% endfor %}
  ],

  // This is the list of admin question layouts shown in the administrative
  // user interface. If the list is empty, question layouts will not be shown
  // as a configurable option
  shownAdminQuestionLayouts: [
    {% if config.sequent_ui.shown_admin_question_layouts %}
      {% for item in config.sequent_ui.shown_admin_question_layouts %}
        "{{ item  }}"{% if not loop.last %},{% endif %}
      {% endfor %}
    {% endif %}
  ],

  // This is the list of admin question voting systems shown in the
  // administrative user interface. If the list is empty, question layouts
  // will not be shown as a configurable option
  shownAdminQuestionVotingSystems: [
    {% if config.sequent_ui.shown_admin_question_voting_systems %}
      {% for item in config.sequent_ui.shown_admin_question_voting_systems %}
        "{{ item  }}"{% if not loop.last %},{% endif %}
      {% endfor %}
    {% endif %}
  ],

  // admin fields
  adminFields: [
      {% for field in config.sequent_ui.admin_fields %}

      {
          name: "{{ field.name }}",
      {% if field.label is defined %}

          label: "{{ field.label }}",
      {% endif %}
      {% if field.description is defined %}

          description: "{{ field.description }}",
      {% endif %}
      {% if field.placeholder is defined %}

          placeholder: "{{ field.placeholder }}",
      {% endif %}
      {% if field.min is defined %}

          min: {{ field.min }},
      {% endif %}
      {% if field.max is defined %}

          max: {{ field.max }},
      {% endif %}
      {% if field.step is defined %}

          step: {{ field.step }},
      {% endif %}
      {% if field.value is string %}

          value: "{{ field.value }}",
      {% else %}

          value: {{ field.value }},
      {% endif %}
      {% if field.required is defined %}

          required: {% if field.required %}true{% else %}false{% endif %},
      {% endif %}
      {% if field.private is defined %}

          private: true,
      {% endif %}

          type: "{{ field.type }}"
      }{% if not loop.last %},{% endif %}
      {% endfor %}

  ],

  // Information regarding OpenID Connect authentication
  openIDConnectProviders: [
      {% for provider in config.iam.openid_connect_providers %}
      {
        {% for key, value in provider.public_info.items() %}
          "{{key}}": "{{value}}"{% if not loop.last %},{% endif %}
        {% endfor %}
      }{% if not loop.last %},{% endif %}
      {% endfor %}
  ],

  //Minimum loading time (milliseconds)
  minLoadingTime: {{ config.sequent_ui.min_loading_time }},

  // gui-admin allows to import users from a csv, importing users in batches
  // this parameter sets the batch size
  // 0 means doing the import in only one batch always
  // allowed values: integer number >= 0
  censusImportBatch: {{ config.sequent_ui.census_import_batch|int }},

  resourceUrlWhitelist: [
    // Allow same origin resource loads.
    'self',

    // Allow loading from our assets domain.  Notice the difference between * and **.
    // Uncomment the following to allow youtube videos
    //
    // 'https://www.youtube.com/**',
    // 'https://youtube.com/**'
  ],

  // i18next language options, see http://i18next.com/pages/doc_init.html for
  // details
  i18nextInitOptions: {
    // Default language of the application.
    //
    // Default: 'en'
    //
    language: "{{ config.sequent_ui.language }}",


    // Forces a specific language.
    //
    // Default: not set
    //
    {% if config.sequent_ui.forceLanguage %}
    lng: "{{ config.sequent_ui.language }}",
    {% endif %}


    // specifies the set language query string.
    //
    // Default: "lang"
    //
    detectLngQS: '{{ config.sequent_ui.detectLanguageQueryString }}',


    // Specifies what translations will be available.
    //
    // Default: ['en', 'es', 'gl', 'ca']
    //
    lngWhitelist: [
      {% for lang in config.sequent_ui.languagesWhitelist %}
      '{{lang}}'{% if not loop.last %},{% endif %}
      {% endfor %}
    ],
  },

  // specifies the language cookie options,
  // see https://github.com/ivpusic/angular-cookie#options
  i18nextCookieOptions: {
    // Expiration in days
    //
    // Default: 360
    //
    // expires: 360,


    // Cookie domain
    //
    // Default: not set
    //
    // domain: 'foobar',
  },

  // configure $locationProvider.html5Mode
  // see https://code.angularjs.org/1.2.28/docs/guide/$location
  //
  // Default: false
  // locationHtml5mode: false,
  locationHtml5mode: true,

  // If no Route is set, this is the route that will be loaded
  //
  // Default: '/admin/login'
  defaultRoute: '{{ config.sequent_ui.defaultRoute }}',

  timeoutSeconds: {% if config.sequent_ui.cookies_expires %}{{ config.sequent_ui.cookies_expires * 60 }}{% else %}3600{% endif %},

  {% if config.sequent_ui.custom_public_download_url %}
  publicURL: "{{ config.sequent_ui.custom_public_download_url }}",
  {% else %}
  publicURL: "https://{{config.ballot_box.domain}}/elections/public/",
  {% endif %}

  // if we are in debug mode or not
  debug: {{ config.sequent_ui.debug }},

  // contact data where users can reach to a human when they need it
  contact: {
    // Support contact email displayed in the footer links
    email: "{{ config.sequent_ui.contact.email }}",
    // Sales contact email displayed in the footer links
    sales: "{{ config.sequent_ui.contact.sales }}",
    tlf: "{{ config.sequent_ui.contact.tlf }}"
  },

  // default authentication message to be sent to users of an election
  auth_msg: {
    // authentication message (both for email and SMS authentication methods)
    // the default is the i18next string path, which works for multiple languages
    // you can use these and other variables:
    // URL, URL2, CODE, HOME_URL, EVENT_ID... and slugs
    // example: 'Vote in __URL__ with code __CODE__'
    // default: 'avAdmin.auth.emaildef'
    msg: "{{ config.sequent_ui.auth_msg.msg }}",
    // authentication message subject (for emails)
    // example: "Vote now with Sequent"
    // default: 'avAdmin.auth.emailsubdef'
    subject: "{{ config.sequent_ui.auth_msg.subject }}"
  },

  // social networks footer links
  social: {
      facebook: "{{ config.sequent_ui.social.facebook }}",
      twitter: "{{ config.sequent_ui.social.twitter }}",
      twitterHandle: "{{ config.sequent_ui.social.twitterHandle }}",
      googleplus: "{{ config.sequent_ui.social.googleplus }}",
      youtube: "{{ config.sequent_ui.social.youtube }}",
      github: "{{ config.sequent_ui.social.github }}"
  },

  auth_methods: [
    {% for auth_method in config.sequent_ui.shown_auth_methods %}
    "{{ auth_method }}"{% if not loop.last %},{% endif %}
    {% endfor %}
  ],

  // technology footer links
  technology: {
    aboutus: "{{ config.sequent_ui.technology.aboutus }}",
    pricing: "{{ config.sequent_ui.technology.pricing }}",
    overview: "{{ config.sequent_ui.technology.overview }}",
    solutions: "{{ config.sequent_ui.technology.solutions }}",
    documentation: "{{ config.sequent_ui.technology.documentation }}"
  },

  // legality footer links
  legal: {
    terms_of_service: "{{ config.sequent_ui.legal.terms_of_service }}",
    cookies: "{{ config.sequent_ui.legal.cookies }}",
    privacy: "{{ config.sequent_ui.legal.privacy }}",
    security_contact: "{{ config.sequent_ui.legal.security_contact }}",
    community_website: "{{ config.sequent_ui.legal.community_website }}"
  },

  documentation: {
    show_help:  {% if config.sequent_ui.documentation.show_help %}true{% else %}false{% endif %},
    faq: "{{ config.sequent_ui.documentation.faq }}",
    overview: "{{ config.sequent_ui.documentation.overview }}",
    technical: "{{ config.sequent_ui.documentation.technical }}",
    security_contact: "{{ config.sequent_ui.legal.security_contact }}"
  },

  share_social: {
    allow_edit: {% if config.sequent_ui.share_social.allow_edit %}true{% else %}false{% endif %},
    default: [
      {% for button in config.sequent_ui.share_social.default %}
      {
        network: "{{ button.network }}",
        button_text: "{{ button.button_text }}",
        social_message: "{{ button.social_message }}"
      }{% if not loop.last %},{% endif %}
      {% endfor %}
    ]
  },

  documentation_html_include: "{{ config.sequent_ui.texts.documentation_html_include | regex_replace("\n", "") }}",

  legal_html_include: "{{ config.sequent_ui.texts.legal_html_include | regex_replace("\n", "") }}",

  // Details pertaining to the organization that runs the software
  organization: {
    // Name of the organization, appears in the logo mouse hover, in the login
    // page ("Login into __NAME__ admin account"), in the poweredBy, etc
    orgName: '{{ config.sequent_ui.organization.name }}',

    // Subtitle of the organization, used in the ballot ticket PDF
    orgSubtitle: '{{ config.sequent_ui.organization.subtitle }}',

    //  Big logo of the organization, used in the ballot ticket PDF
    orgBigLogo: '{{ config.sequent_ui.organization.big_logo_url }}',

    // URL that the logo links to
    orgUrl: '{{ config.sequent_ui.organization.url }}'
  },

  verifier: {
    link: "",
    hash: ""
  },

  success: {
    text: "{{ config.sequent_ui.texts.booth_success_extra | regex_replace("\n", "") }}"
  },

  tos: {
    text:"{{ config.sequent_ui.texts.tos_text }}",
    title: "{{ config.sequent_ui.texts.tos_title }}"
  },

  mainVersion: "{{ config.sequent_ui.mainVersion }}",
  repoVersions: [
    {% for key, value in repos.items() %}
    {
      repoName: "{{ key }}",
      repoVersion: "{{ value.version }}"
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ],

  {% if config.sequent_ui.cookies_expires %}
    cookies: {
      expires: {{ config.sequent_ui.cookies_expires }},
    },
  {% endif %}

  {% if config.sequent_ui.browser_update_config %}
    // Browser update configuration. See https://browser-update.org
    browserUpdate: {{ config.sequent_ui.browser_update_config }}
  {% endif %}

};

angular.module('SequentConfig', [])
  .factory('ConfigService', function() {
    return SequentConfigData;
  });

angular.module('SequentConfig')
  .provider('ConfigService', function ConfigServiceProvider() {
    _.extend(this, SequentConfigData);

    this.$get = [function ConfigServiceProviderFactory() {
    return new ConfigServiceProvider();
    }];
  });
