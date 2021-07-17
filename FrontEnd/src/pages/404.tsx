import React, { FunctionComponent, useEffect } from 'react';
import { TriggerPageView } from '@components/ga';
import { Head } from '@basics';

const Custom404: FunctionComponent = () => {
  useEffect(() => {
    TriggerPageView('404');
  }, []);

  return (
    <>
      <Head title="404" />
      <h1>404 - Page not found</h1>;
    </>
  );
};

export default Custom404;
