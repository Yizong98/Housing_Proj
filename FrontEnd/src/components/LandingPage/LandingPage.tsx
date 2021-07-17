import React, { FunctionComponent, useEffect } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import { landingIcons } from '@icons';
import styles from './LandingPage.module.scss';
import Button from '@components/basics/Button';
import { useRouter } from 'next/dist/client/router';
import { TriggerPageView } from '@components/ga';

const HomehubWelcomeInfo: FunctionComponent = () => {
  const router = useRouter();
  const routeToHouseListings = () => {
    router.push('/housing', undefined, { shallow: true });
  };

  useEffect(() => {
    TriggerPageView('landing_page');
  }, []);

  return (
    <div className={styles.title}>
      <div className={styles.bigRow}>
        <landingIcons.logo className={styles.logo} />{' '}
        <span className={styles.logoText}>Homehub</span>
      </div>
      <div className={styles.bigRow}>
        <div className={styles.text}>
          Find your ideal home away from home ASAP
        </div>
      </div>
      <div className={styles.bigRow}>
        <div className={styles.subtext}>
          By students <span className={styles.dot}></span> For students{' '}
          <span className={styles.dot}></span> With students
        </div>
      </div>
      <div className={styles.center}>
        <Button onClick={routeToHouseListings}>
          <div className={styles.buttonInner}>Check it Out</div>
        </Button>
      </div>
    </div>
  );
};

const WhyHomeHubInfo: FunctionComponent = () => (
  <Row className={styles.iconRow}>
    <Col className={styles.introCol}>
      <Row className={styles.smallRow}>
        <landingIcons.safety className={styles.smallImg} />
      </Row>
      <Row className={styles.caption}>Safety</Row>
      <div className={styles.textSm}>
        Homehub <b>requires a “@ucsd. edu” email address</b> to create an
        account and interact with listings by other students.
      </div>
    </Col>
    <Col className={styles.introCol}>
      <Row className={styles.smallRow}>
        <landingIcons.efficiency className={styles.smallImg} />
      </Row>
      <Row className={styles.caption}>Efficiency</Row>
      <div className={styles.textSm}>
        Finding a home that fits all your needs is <b>easy and quick </b>
        through our smart <b>filter & match</b> and search options.
      </div>
    </Col>
    <Col className={styles.introCol}>
      <Row className={styles.smallRow}>
        <landingIcons.community className={styles.smallImg} />
      </Row>
      <Row className={styles.caption}>Community</Row>
      <div className={styles.textSm}>
        After signing up, you will be grouped with peer students at UCSD to
        <b> get more involved with others in the community.</b>
      </div>
    </Col>
  </Row>
);

const Landing: FunctionComponent = () => {
  const router = useRouter();
  const routeToHouseListings = () => {
    router.push('/housing', undefined, { shallow: true });
  };

  return (
    <Container className={styles.container}>
      <HomehubWelcomeInfo></HomehubWelcomeInfo>

      <Row className={styles.intro}>
        <Col className={styles.housingicon}>
          <landingIcons.housing />
        </Col>
        <Col className={styles.textIntro}>
          <div className={styles.textLg}>What is Homehub?</div>
          <div className={styles.subtextIntro}>
            Homehub connects students with their peers within UCSD to create a
            reliable housing network for college students to find great places
            to live.
          </div>
        </Col>
      </Row>

      <Row className={styles.intro}>
        <Row className={styles.bigRow}>
          <div className={styles.textLg}>Why Homehub?</div>
        </Row>
        <WhyHomeHubInfo></WhyHomeHubInfo>
        <Row className={styles.center}>
          <Button onClick={routeToHouseListings}>
            <div className={styles.buttonInner}>Check it Out</div>
          </Button>
        </Row>
      </Row>
    </Container>
  );
};

export default Landing;
