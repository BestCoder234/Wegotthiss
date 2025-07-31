import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html>
      <Head>
        {/* PostHog Analytics */}
        <script
          dangerouslySetInnerHTML={{ __html: `
            !(function(t,e){var o,n,p,r;e.__SV=0,e.posthog=e.posthog||[],e.posthog._i=[],e.posthog.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(n=t.createElement("script"),n.type="text/javascript",n.async=!0,n.src="https://cdn.posthog.com/posthog.js",(p=t.getElementsByTagName("script")[0]).parentNode.insertBefore(n,p),r=e.posthog);var t=e.posthog;t.init('<YOUR_POSTHOG_API_KEY>',{api_host:'https://app.posthog.com'});` }}
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
} 