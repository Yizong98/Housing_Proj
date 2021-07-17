import React, { FunctionComponent, useEffect } from 'react';
import type { AppProps } from 'next/app';
import { reduxNextWrapper } from '@redux';
import Login from '@components/Login';
import '../assets/scss/global/index.scss';
import Layout from '@components/Layout';
import { InitGA } from '@components/ga';
import TagManager from 'react-gtm-module';
import { Head as DefaultHead } from '@basics';

const App: FunctionComponent<AppProps> = ({ Component, pageProps }) => {
  const tagManagerArgs = {
    gtmId: 'GTM-KRRW5N3',
    dataLayer: {
      page: 'home',
    },
  };

  useEffect(() => {
    InitGA();
    TagManager.initialize(tagManagerArgs);
  }, []);

  return (
    <>
      <DefaultHead />

      <Login />

      <Layout>
        <Component {...pageProps} />
      </Layout>
    </>
  );
};

export default reduxNextWrapper.withRedux(App);
