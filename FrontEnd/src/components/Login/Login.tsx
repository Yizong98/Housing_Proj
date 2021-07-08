import React, { FunctionComponent } from 'react';
import { Modal, Button, Tooltip, Caption } from '@basics';
import {
  GoogleLogin,
  GoogleLoginResponse,
  GoogleLoginResponseOffline,
} from 'react-google-login';
import { useDispatch } from 'react-redux';
import { useShouldShowLogin, hideLogin, startNewUserFlow } from '@redux';
import { miscIcons } from '@icons';
import styles from './Login.module.scss';
import NewUserSetup from '@components/NewUserSetup';
import { useUser } from '@hooks';
import { TriggerButtonGA } from '@components/ga';
import UnsupportedDomainPopup from './UnsupportedDomainPopup/UnsupportedDomainPopup';

// Used in tooltip as the title
const TooltipContent = (
  <span>
    We use school email addresses to ensure all users are current students of
    universities in an attempt to{' '}
    <b>enhance reliability and credibility of posts</b>.
  </span>
);

const isOnline = (
  response: GoogleLoginResponse | GoogleLoginResponseOffline,
): response is GoogleLoginResponse => 'profileObj' in response;

// https://developers.google.com/identity/sign-in/web/sign-in
const LoginUI: FunctionComponent = () => {
  const dispatch = useDispatch();
  const shouldShowLogin = useShouldShowLogin();
  const { login } = useUser();

  const responseGoogleSuccess = async (
    response: GoogleLoginResponse | GoogleLoginResponseOffline,
  ) => {
    if (isOnline(response)) {
      const { profileObj: userInfo, tokenId } = response;
      const { name, email } = userInfo;

      const result = await login(tokenId);
      if (result.unsupportedDomain) {
        // TODO this should display the not supported modal
        // trigger event that user login fails
        console.log("Unsupported - result failed");
        return;
      }
      if (result.isNewUser) {
        TriggerButtonGA('Button', 'Click', 'LogInNewUser');
        dispatch(startNewUserFlow({ name, email }));
        return;
      }
      TriggerButtonGA('Button', 'Click', 'LogInSuccess');
    } else {
      console.log('User is offline');
      console.log(response);
    }
  };

  return (
    <Modal
      open={shouldShowLogin}
      onClose={() => dispatch(hideLogin())}
      className={styles.wrapper}
    >
      <div>
        <Button variant="wrapper" onClick={() => dispatch(hideLogin())}>
          <miscIcons.orangeX />
        </Button>
      </div>

      <div className="d-flex justify-content-center">
        <img className={styles.loginImg} src="/login.svg" alt="LogIn" />
      </div>

      <GoogleLogin
        className={styles.gAuth}
        clientId="778916194800-977823s60p7mtu1sj72ru0922p2pqh6m.apps.googleusercontent.com"
        onSuccess={async (response) => {
          await responseGoogleSuccess(response);
          dispatch(hideLogin());
        }}
        cookiePolicy="single_host_origin"
        icon={false}
      >
        <Button
          icon={{ icon: miscIcons.GoogleLogo }}
          onClick={() => TriggerButtonGA('Button', 'Click', 'LogIn')}
        >
          Start with school account
        </Button>
      </GoogleLogin>

      <Tooltip title={TooltipContent}>Why school account?</Tooltip>
    </Modal>
  );
};

const Login: FunctionComponent = () => {
  const { data: user } = useUser();

  // if user is logged in, there's no need to render the login component
  if (user.isLoggedIn) return null;

  return (
    <>
      <LoginUI />
      <NewUserSetup />
      <UnsupportedDomainPopup />
    </>
  );
};

export default Login;
