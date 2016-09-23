/**
 * This file is part of agora-dev-box.
 * Copyright (C) 2014-2016  Agora Voting SL <agora@agoravoting.com>

 * agora-dev-box is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License.

 * agora-dev-box is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.

 * You should have received a copy of the GNU Affero General Public License
 * along with agora-dev-box.  If not, see <http://www.gnu.org/licenses/>.
**/

/*
 * ConfigService is a function that returns the configuration that exists
 * in this same file, which you might want to edit and tune if needed.
 */

var AV_CONFIG_VERSION = '3.3.0';

var avConfigData = {
  // the base url path for ajax requests, for example for sending ballots or
  // getting info about an election. This url is usually in the form of
  // 'https://foo/api/v3/' and always ends in '/'.
  base: '',
  theme: "{{ config.agora_gui.theme }}",
  baseUrl: "https://{{config.agora_elections.domain}}/elections/api/",
  freeAuthId: 1,
  
  // Webpage title
  webTitle: "{{ config.agora_gui.web_title }}",
  
  // Show 'Success Action' tab in admin agora_gui
  showSuccessAction: {% if config.agora_gui.show_success_action %}true{% else %}false{% endif %},

  // AuthApi base url
  authAPI: "https://{{config.agora_elections.domain}}/authapi/api/",
  dnieUrl: "https://agora.dev/authapi/api/authmethod/dnie/auth/",
  // Agora Elections base url
  electionsAPI: "https://{{config.agora_elections.domain}}/elections/api/",

  // Agora Admin help url
  helpUrl: "{{ config.agora_gui.technology.admin_manual }}",

  authorities: {{ config.auths }},
  director: "{{ config.director }}",

  //Minimum loading time (milliseconds)
  minLoadingTime: {{ config.agora_gui.min_loading_time }},

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
    language: "{{ config.agora_gui.language }}",


    // Forces a specific language.
    //
    // Default: not set
    //
    lng: "{{ config.agora_gui.language }}",


    // specifies the set language query string.
    //
    // Default: "lang"
    //
    detectLngQS: 'lang',


    // Specifies what translations will be available.
    //
    // Default: ['en', 'es', 'gl', 'ca']
    //
    // lngWhitelist: ['en', 'es', 'gl', 'ca'],
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
  defaultRoute: '{{ config.agora_gui.defaultRoute }}',

  timeoutSeconds: 3600,

  {% if config.agora_gui.custom_public_download_url %}
  publicURL: "{{ config.agora_gui.custom_public_download_url }}",
  {% else %}
  publicURL: "https://{{config.agora_elections.domain}}/elections/public/",
  {% endif %}

  // if we are in debug mode or not
  debug: {{ config.agora_gui.debug }},

  // contact data where users can reach to a human when they need it
  contact: {
    // Support contact email displayed in the footer links
    email: "{{ config.agora_gui.contact.email }}",
    // Sales contact email displayed in the footer links
    sales: "{{ config.agora_gui.contact.sales }}",
    tlf: "{{ config.agora_gui.contact.tlf }}"
  },

  // social networks footer links
  social: {
      facebook: "{{ config.agora_gui.social.facebook }}",
      twitter: "{{ config.agora_gui.social.twitter }}",
      twitterHandle: "{{ config.agora_gui.social.twitterHandle }}",
      googleplus: "{{ config.agora_gui.social.googleplus }}",
      youtube: "{{ config.agora_gui.social.youtube }}",
      github: "{{ config.agora_gui.social.github }}"
  },

  // technology footer links
  technology: {
    aboutus: "{{ config.agora_gui.technology.aboutus }}",
    pricing: "{{ config.agora_gui.technology.pricing }}",
    overview: "{{ config.agora_gui.technology.overview }}",
    solutions: "{{ config.agora_gui.technology.solutions }}",
    admin_manual: "{{ config.agora_gui.technology.admin_manual }}"
  },

  // legality footer links
  legal: {
    terms_of_service: "{{ config.agora_gui.legal.terms_of_service }}",
    cookies: "{{ config.agora_gui.legal.cookies }}",
    privacy: "{{ config.agora_gui.legal.privacy }}",
    security_contact: "{{ config.agora_gui.legal.security_contact }}",
    community_website: "{{ config.agora_gui.legal.community_website }}"
  },

  documentation: {
    faq: "{{ config.agora_gui.documentation.faq }}",
    overview: "{{ config.agora_gui.documentation.overview }}",
    technical: "{{ config.agora_gui.documentation.technical }}",
    security_contact: "{{ config.agora_gui.legal.security_contact }}"
  },

  share_social: {
    allow_edit: {% if config.agora_gui.share_social.allow_edit %}true{% else %}false{% endif %},
    default: [
      {% for button in config.agora_gui.share_social.default %}
      {
        network: "{{ button.network }}",
        button_text: "{{ button.button_text }}",
        social_message: "{{ button.social_message }}"
      }{% if not loop.last %},{% endif %}
      {% endfor %}
    ]
  },

  documentation_html_include: "{{ config.agora_gui.texts.documentation_html_include }}",

  legal_html_include: "{{ config.agora_gui.texts.legal_html_include }}",

  // Details pertaining to the organization that runs the software
  organization: {
    // Name of the organization, appears in the logo mouse hover, in the login
    // page ("Login into __NAME__ admin account"), in the poweredBy, etc
    orgName: '{{ config.agora_gui.organization.name }}',

    // URL that the logo links to
    orgUrl: '{{ config.agora_gui.organization.url }}'
  },

  verifier: {
    link: "",
    hash: ""
  },

  success: {
    text: "{{ config.agora_gui.texts.booth_success_extra }}"
  },

  tos: {
    text:"{{ config.agora_gui.texts.tos_text }}",
    title: "{{ config.agora_gui.texts.tos_title }}"
  }
};

angular.module('avConfig', [])
  .factory('ConfigService', function() {
    return avConfigData;
  });

angular.module('avConfig')
  .provider('ConfigService', function ConfigServiceProvider() {
    _.extend(this, avConfigData);

    this.$get = [function ConfigServiceProviderFactory() {
    return new ConfigServiceProvider();
    }];
  });
