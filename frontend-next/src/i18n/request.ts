import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async () => {
  // Provide a static locale for now, can be dynamic based on user preference
  const locale = 'en';

  return {
    locale,
    messages: (await import(`./messages/${locale}.json`)).default,
  };
});
