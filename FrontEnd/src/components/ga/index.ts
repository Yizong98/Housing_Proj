import React from 'react';
import ReactGA from 'react-ga';


export const InitGA = () => {
    ReactGA.initialize('UA-199317849-1');
}

export const TriggerPageView = ( pageName:string ) => {
    ReactGA.pageview(pageName);
}

/**
 * TriggerButtonGA - Add custom tracking event
 */
 export const TriggerButtonGA = (category:string, action:string, label:string) => {
    ReactGA.event({
      category: category,
      action: action,
      label: label
    });
  };




