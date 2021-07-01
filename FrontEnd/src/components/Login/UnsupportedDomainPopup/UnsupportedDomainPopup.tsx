import React, { FunctionComponent } from 'react';
import { Modal, Button } from '@basics';
import { useDispatch } from 'react-redux';
import { useShowUnsupportedDomainPopup, hideUnsupportedDomainPopup } from '@redux';
import { miscIcons } from '@icons';
import styles from './UnsupportedDomainPopup.module.scss';
import { useUser } from '@hooks';

const UnsupportedDomainPopupUI: FunctionComponent = () => {
  const { data: user } = useUser();
  const dispatch = useDispatch();
  const shouldShowUnsupportedDomainPopup = useShowUnsupportedDomainPopup();

  // if user is logged in, there's no need to render the login component
  if (user.isLoggedIn) return null;


  return (
    <Modal
      open={shouldShowUnsupportedDomainPopup}
      onClose={() => dispatch(hideUnsupportedDomainPopup())}
      className={styles.wrapper}
    >

      <div>
        <Button variant="wrapper" onClick={() => dispatch(hideUnsupportedDomainPopup())}>
          <miscIcons.orangeX />
        </Button>
      </div>


      <div className="d-flex justify-content-center border-0">
        <img className={styles.loginImg} src="/triton.svg" alt="LogInNotSupported" />
      </div>

      <div className="d-flex flex-column align-items-center text-center">
        <div className={styles.firstMessage}>
          Oops, your email is incorrect...
        </div>
        <div className="px-4">
          At the moment, we only allow email ends with <strong>ucsd.edu</strong> to sign up!
        </div>

        <div className="flex-row">

        </div>
      </div>
        
    </Modal>
  );
};

const UnsupportedDomainPopup: FunctionComponent = () => {
  const { data: user } = useUser();

  // if user is logged in, there's no need to render the login component
  if (user.isLoggedIn) return null;

  return (
    <>
      <UnsupportedDomainPopupUI />
    </>
  );
};

export default UnsupportedDomainPopup;
