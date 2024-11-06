// https://docusaurus.io/docs/api/docusaurus-config#i18n
// workaround for 'baseUrl—customization of base URL is a work-in-progress.'
export default function onRouteUpdate({ location }) {
  const prefix = '/jp/en/';
  if (location.pathname.startsWith(prefix)) {
    const newPath = location.pathname.replace(prefix, '/');
    window.location.replace(newPath);
  }
}
