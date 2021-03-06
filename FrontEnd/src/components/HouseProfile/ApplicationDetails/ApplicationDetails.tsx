import React, { FunctionComponent, useState, useEffect } from 'react';
import styles from './ApplicationDetails.module.scss';
import styles_parent from '../HouseProfile.module.scss'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import { Subtitle1, Subtitle2, Body2, Link } from '@basics';
import { profileIcons } from '@icons';
import { useLandlordRoomData } from '@hooks';
import { getDurationInMinutes } from '@apis';
import SectionTitle from '../SectionTitle/SectionTitle';
import ProofOfIncome from './ProofOfIncome/ProofOfIncome';

interface ApplicationDetailsProps {
  roomId: number;
}

const ApplicationDetails: FunctionComponent<ApplicationDetailsProps> = ({
  roomId,
}) => {
  const { data, error } = useLandlordRoomData(roomId);
  // console.log(getDurationInMinutes("7936 Avenida Navidad San Diego, CA 92122"));

  if (error) {
    return <div>Error occurred!</div>; // TODO handle error in a different way
  }

  if (!data) {
    return <div>Loading How to Apply...</div>; // TODO add a loader
  }

  const {
    applicationFee,
    holdingPeriod,
    holdingDeposit,
    housingDeposit,
    verification,
    proofOfIncome,
    website,
  } = data;

  // Used in ApplicationDetails to display information with labels
  const details = {
    'Application Fee': (
      <div className="d-flex">
        {applicationFee}
        <Link href={website} external className={styles.applyNowLink}>
          Apply Now
        </Link>
      </div>
    ),
    'Holding Period': holdingPeriod,
    'Holding Deposit': holdingDeposit,
    'Housing Deposit': housingDeposit,
    Verification: verification,
  };

  // Changes details specified above into appropriate text + columns
  const ApplicationDetailTiles: FunctionComponent = () => (
    <Row className={styles.applicationDetailTiles}>
      {Object.entries(details).map(([label, value]) => (
        <Col xs={12} md={4} className="py-3 pr-md-3">
          <Subtitle2>{label}</Subtitle2>
          <Body2>{value}</Body2>
        </Col>
      ))}
    </Row>
  );

  return (
    <Container className={styles_parent.container}>
      <Row>
        <Col>
          <SectionTitle>To Apply</SectionTitle>
        </Col>
        
        <ApplicationDetailTiles />

        <ProofOfIncome proofOfIncome={proofOfIncome} />
      </Row>
    </Container>
  );
};

export default ApplicationDetails;
