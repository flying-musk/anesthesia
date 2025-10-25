export function StructuredData() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Anesthesia Management System',
    applicationCategory: 'HealthApplication',
    operatingSystem: 'Web',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
    },
    description:
      'AI-Powered Anesthesia Guidelines Generation System with multi-language support for healthcare professionals.',
    featureList: [
      'Patient Management',
      'AI-Powered Guideline Generation',
      'Multi-language Support',
      'Medical History Tracking',
      'Real-time Updates',
    ],
    softwareVersion: '1.0.0',
    author: {
      '@type': 'Organization',
      name: 'Anesthesia Management Team',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '125',
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
    />
  );
}
