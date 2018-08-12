module.exports = {
    locales: {
        '/': {
            lang: 'en-US',
            title: 'Django Zero',
            description: 'Django projects with (nearly) zero configuration. Comes bundled with preconfigured Webpack, Bootstrap, SASS, Jinja2, Allauth and more.'
        },
    },
    head: [
        ['link', {rel: 'icon', href: `/logo.png`}],
        ['link', {rel: 'manifest', href: '/manifest.json'}],
        ['meta', {name: 'theme-color', content: '#3eaf7c'}],
        ['meta', {name: 'apple-mobile-web-app-capable', content: 'yes'}],
        ['meta', {name: 'apple-mobile-web-app-status-bar-style', content: 'black'}],
        ['link', {rel: 'apple-touch-icon', href: `/icons/apple-touch-icon-152x152.png`}],
        ['link', {rel: 'mask-icon', href: '/icons/safari-pinned-tab.svg', color: '#3eaf7c'}],
        ['meta', {name: 'msapplication-TileImage', content: '/icons/msapplication-icon-144x144.png'}],
        ['meta', {name: 'msapplication-TileColor', content: '#000000'}]
    ],
    serviceWorker: true,
    themeConfig: {
        repo: 'django-zero/django-zero',
        editLinks: true,
        docsDir: 'docs',
        locales: {
            '/': {
                label: 'English',
                selectText: 'Languages',
                editLinkText: 'Edit this page on GitHub',
                lastUpdated: 'Last Updated',
                serviceWorker: {
                    updatePopup: {
                        message: "New content is available.",
                        buttonText: "Refresh"
                    }
                },
                nav: [
                    {text: 'Home', link: '/'},
                    {text: 'Quick Start', link: '/getting-started'},
                    {text: 'Guides', link: '/guides/'},
                    {text: 'How-To', link: '/howto/'},
                ],
                sidebar: {
                    '/guides/': [
                        {
                            title: 'Guides',
                            collapsable: false,
                            children: [
                                '',
                                'cli',
                                'templating',
                                'frontend',
                                'tests',
                                'users',
                                'deployment',
                            ]
                        }
                    ],
                    '/howto/': [
                        {
                            title: 'How-To',
                            collapsable: false,
                            children: [
                                'create-an-application',
                            ]
                        }
                    ],
                    '/created/': [
                        {
                            title: 'Just Created ❤',
                            collapsable: false,
                            children: [
                                'project',
                                'app',
                            ]
                        }
                    ],
                    '/': [
                        {
                            title: 'Django Zero',
                            collapsable: false,
                            children: [
                                '',
                                'install',
                                'getting-started',
                                'guides/',
                                'howto/',
                                'contributions',
                            ]
                        }
                    ]
                }
            }
        }
    }
}

