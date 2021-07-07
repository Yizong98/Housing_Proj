import React, { FunctionComponent } from 'react';
import { Modal, Button, Body2, Caption, Input } from '@basics';
import { useDispatch } from 'react-redux';
import {
  useShowUnsupportedDomainPopup,
  hideUnsupportedDomainPopup,
  useShowReportIssue,
  showReportIssue,
  hideReportIssue,
} from '@redux';
import { miscIcons } from '@icons';
import styles from './UnsupportedDomainPopup.module.scss';
import { useUser } from '@hooks';
import { Col, Row } from 'react-bootstrap';

const UnsupportedDomainPopupUI: FunctionComponent = () => {
  const { data: user } = useUser();
  const dispatch = useDispatch();
  const shouldShowUnsupportedDomainPopup = useShowUnsupportedDomainPopup();
  const shouldShowReportIssue = useShowReportIssue();

  // if user is logged in, there's no need to render the login component
  if (user.isLoggedIn) return null;

  return (
    <Modal
      open={shouldShowUnsupportedDomainPopup}
      onClose={() => dispatch(hideUnsupportedDomainPopup())}
      className={styles.wrapper}
    >
      <div>
        <Button
          variant="wrapper"
          onClick={() => dispatch(hideUnsupportedDomainPopup())}
        >
          <miscIcons.orangeX />
        </Button>
      </div>

      <div className="d-flex justify-content-center">
        <img
          className={styles.loginImg}
          src="/triton.svg"
          alt="LogInNotSupported"
        />
      </div>

      <Col>
        <div className={styles.messages}>
          <div className={styles.firstMessage}>
            Oops, your email is incorrect...
          </div>
          <div className={styles.secondMessage}>
            At the moment, we only allow email ends with{' '}
            <strong>ucsd.edu</strong> to sign up!
          </div>
        </div>

        <div className={styles.bottomRowButtons}>
          <Button
            size="secondary"
            variant="wrapper"
            onClick={() => {
              dispatch(hideUnsupportedDomainPopup());
              dispatch(showReportIssue());
            }}
          >
            <div className={styles.reportIssue}>
              <Body2>Report an issue</Body2>
            </div>
          </Button>
          <Button
            size="secondary"
            variant="outline"
            onClick={() => dispatch(hideUnsupportedDomainPopup())}
          >
            Okay
          </Button>
        </div>
      </Col>
    </Modal>
  );
};

const AfterReportIssueUI: FunctionComponent = () => {
  const { data: user } = useUser();
  const dispatch = useDispatch();
  const shouldShowReportIssue = useShowReportIssue();

  // if user is logged in, there's no need to render the login component
  if (user.isLoggedIn) return null;

  return (
    <Modal
      open={shouldShowReportIssue}
      onClose={() => dispatch(hideReportIssue())}
      className={styles.wrapper}
    >
      <div>
        <Button variant="wrapper" onClick={() => dispatch(hideReportIssue())}>
          <miscIcons.orangeX />
        </Button>
      </div>

      <Col className={styles.reportIssueWrapper}>
        <div className={styles.reportIssueLabel}>Report issue</div>

        <Row>
          <miscIcons.orangeWrench className={styles.wrenchIcon} />
          <Caption className={styles.wrenchIconCaption}>
            We will get back to you within 7 work days! Thanks for using Homehub
            ;)
          </Caption>
        </Row>

        <div className="d-flex justify-content-center pt-3 pb-4">
          <Input
            className={styles.input}
            type="text"
            placeholder="please input your email"
          />
        </div>

        <Button
          size="secondary"
          variant="outline"
          onClick={() =>
            alert(
              'TODO - send an email to Cris’ email \nTitle: [Homehub]Issue reported \nContent: {user’s email} has issued an report. please handle within 7 work days',
            )
          }
        >
          Send report
        </Button>
      </Col>
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
      <AfterReportIssueUI />
    </>
  );
};

export default UnsupportedDomainPopup;
