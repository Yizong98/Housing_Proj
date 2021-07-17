import React, { FunctionComponent } from 'react';
import NextHead from 'next/head';

export interface HeadProps {
  title?: string; // title of the page displayed. Will be appended with `| Homehub`
  additionalKeywords?: string[]; // keywords to append to the keywords metadata
  description?: string; // description of the page
}

/**
 * Head is a wrapper component for NextJS's Head, which allows to set meta data and
 * title of the website.
 *
 * Pass custom meta data through children. Note: you should set the "key" prop though
 * to avoid duplications (https://nextjs.org/docs/api-reference/next/head)
 */
const Head: FunctionComponent<HeadProps> = ({
  title,
  description = 'Find your ideal home away from home ASAP. By students, for students, with students.',
  additionalKeywords = [],
  children,
}) => (
  <NextHead>
    {title ? <title>{title} | Homehub</title> : <title>Homehub</title>}

    <meta
      name="viewport"
      content="width=device-width, initial-scale=1"
      key="viewport"
    />
    <meta name="description" content={description} key="description" />
    <meta
      name="keywords"
      content={`Homehub, Housing, Students, University of California San Diego ${additionalKeywords?.map(
        (k) => `, ${k}`,
      )}`}
      key="keywords"
    />

    {children}
  </NextHead>
);

export default Head;
