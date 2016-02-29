/*
 * ConfigService is a function that returns the configuration that exists
 * in this same file, which you might want to edit and tune if needed.
 */

var AV_CONFIG_VERSION = '3.1.3';

var avConfigData = {
  // the base url path for ajax requests, for example for sending ballots or
  // getting info about an election. This url is usually in the form of
  // 'https://foo/api/v3/' and always ends in '/'.
  base: '',
  theme: "{{ config.agora_gui.theme }}",
  baseUrl: "https://{{config.agora_elections.domain}}/elections/api/",
  freeAuthId: 1,

  // AuthApi base url
  authAPI: "https://{{config.agora_elections.domain}}/authapi/api/",
  dnieUrl: "https://agora.dev/authapi/api/authmethod/dnie/auth/",
  // Agora Elections base url
  electionsAPI: "https://{{config.agora_elections.domain}}/elections/api/",

  // Agora Admin help url
  helpUrl: "{{ config.agora_gui.technology.admin_manual }}",

  authorities: {{ config.auths }},
  director: "{{ config.director }}",

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

  publicURL: "https://{{config.agora_elections.domain}}/elections/public/",

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

  help: {
    info:""
  },

  success: {
    text: ""
  },

  tos: {
    text:"",
    title: ""
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
