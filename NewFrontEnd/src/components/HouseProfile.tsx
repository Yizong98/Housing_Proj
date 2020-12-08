import React, { useEffect, useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import { useDispatch, useSelector } from 'react-redux';
import {
  selectHousingFavorites,
  newHousingFavorite,
  removeHousingFavorite,
} from '../redux/slices/housing';
import GoogleMap from './GoogleMap';
import PreviewSlideShow from './PreviewSlideShow';
import { SlideShowItem } from './SlideShow';
import { contactIcons, miscIcons, facilityIcons } from '../assets/icons/all';
import { LOGIN_TO_VIEW } from '../assets/constants/messages';
import { HousePost } from '../assets/models/PostModels';
import { months } from '../assets/constants';
import {
  removeParentheses,
  abbreviateAddress,
  abbreviateMonth,
  abbreviateMoveIn,
  formatRoomType,
} from '../assets/utils';
import { selectUser } from '../redux/slices/auth';

const Ellipse: React.FC<{}> = () => (
  <Row className="justify-content-center">
    <miscIcons.ellipse className="m-3" />
    <miscIcons.ellipse className="m-3" />
    <miscIcons.ellipse className="m-3" />
  </Row>
);

export const facilityToIcon = {
  Parking: <facilityIcons.parking />,
  Elevator: <facilityIcons.elevator />,
  'Gym room': <facilityIcons.gym />,
  'Swimming pool': <facilityIcons.swimmingPool />,
  'Pets friendly': <facilityIcons.petsFriendly />,
  'Indoor washer': <facilityIcons.indoorWasher />,
};

const GetIcon: React.FC<{ str: keyof typeof facilityToIcon }> = ({ str }) => (
  <div className="mt-2">{facilityToIcon[str]}</div>
);

interface PathProps extends HousePost {
  show: boolean;
  setShow: (show: boolean) => void;
}

const HouseProfile: React.FC<PathProps> = ({
  name,
  pricePerMonth,
  roomType,
  early,
  late,
  distance,
  location,
  photos,
  profilePhoto,
  stayPeriod,
  leaserName,
  leaserSchoolYear,
  leaserMajor,
  leaserIntro,
  leaserEmail,
  leaserPhone,
  roomId,
  other,
  facilities,
  show,
  setShow,
  negotiable,
}) => {
  const favorites = useSelector(selectHousingFavorites);
  const user = useSelector(selectUser);
  const dispatch = useDispatch();
  const [moveIn, setMoveIn] = useState<string>('');
  const [slideShowItems, setSlideShowItems] = useState<SlideShowItem[]>([]);

  // set the slide show content
  useEffect(() => {
    setSlideShowItems(
      photos.map((url) => ({
        src: `https://houseit.s3.us-east-2.amazonaws.com/${url}`,
        alt: `${leaserEmail} , ${location}}`,
      })),
    );
  }, [photos, leaserEmail, location]);

  // abbreviate the move in date
  useEffect(() => {
    const [earlyInt, earlyMonth] = early.split(' ') as [string, months];
    const [lateInt, lateMonth] = late.split(' ') as [string, months];

    // TODO temporary, 'anytime' should not be in the database (same with the removeParentheses)
    const earlyIntDisplayed =
      earlyInt.toLowerCase() === 'anytime'
        ? earlyInt
        : removeParentheses(earlyInt);
    const lateIntDisplayed =
      lateInt.toLowerCase() === 'anytime'
        ? lateInt
        : removeParentheses(lateInt);

    setMoveIn(
      abbreviateMoveIn(
        earlyIntDisplayed,
        earlyMonth,
        lateIntDisplayed,
        lateMonth,
      ),
    );
  }, [early, late]);

  return (
    <Modal
      show={show}
      onHide={() => setShow(false)}
      size="xl"
      centered
      className="house-profile-modal"
    >
      <Container className="p-0 house-profile-container">
        <Row className="h-100">
          {/* first column */}
          <Col sm={12} lg={4}>
            {/* Close button overlay */}
            {/* TODO: margins on top and left */}
            <Button
              variant="no-show"
              onClick={() => setShow(false)}
              className="house-profile-close"
            >
              <miscIcons.greenX />
            </Button>
            <PreviewSlideShow
              items={slideShowItems}
              className="house-profile-preview-slideshow"
            />
          </Col>

          {/* second column */}
          <Col sm={12} md={6} lg={4}>
            {/* mt-3 mt-lg-5 mt-md-4 */}
            <Container className="d-flex flex-column justify-content-around mx-3 mx-lg-0 h-100">
              <Row className="justify-content-left flex-grow-0">
                <span className="housing-profile-house-type">{name}</span>
              </Row>

              <Row>
                <Col className="housing-profile-price" md={5}>
                  <Row>
                    {negotiable && '~'}${pricePerMonth}
                  </Row>
                </Col>
                <Col md={{ span: 5, offset: 2 }}>
                  <Row className="subtitle-text">Room type</Row>
                  <Row className="primary-text">{formatRoomType(roomType)}</Row>
                </Col>
              </Row>

              <Row className="justify-content-center">
                <Col md={5}>
                  <Row className="subtitle-text">Move in time</Row>
                  <Row className="primary-text">{moveIn}</Row>
                </Col>

                <Col md={{ span: 5, offset: 2 }}>
                  <Row className="subtitle-text">Stay period</Row>
                  <Row className="primary-text">{stayPeriod} months</Row>
                </Col>
              </Row>

              <Ellipse />

              <Row className="subtitle-text">Facilities</Row>
              <Row className="subtitle-text">
                {facilities.map((facility) => (
                  <Col
                    xs={{ span: 3, offset: 1 }}
                    key={facility}
                    className="text-center"
                  >
                    <GetIcon str={facility} />
                    {facility}
                  </Col>
                ))}
              </Row>

              <Ellipse />

              <Row className="subtitle-text">Looking for</Row>
              <ul className="primary-text">
                {other.map((description) => (
                  <li key={description}>{description}</li>
                ))}
              </ul>
            </Container>
          </Col>

          {/* third column */}
          <Col sm={12} md={6} lg={4} className="d-flex flex-column mt-3">
            <div className="house-profile-top-half">
              <Row>
                <Col xs={8} className="justify-content-center">
                  <Button
                    variant="tertiary"
                    block
                    onClick={() => {
                      const housePost = {
                        // TODO change the prop vars to be the same name as HouseCard
                        photos,
                        name,
                        pricePerMonth,
                        roomType,
                        early,
                        late,
                        stayPeriod,
                        facilities,
                        other,
                        distance,
                        location,
                        leaserName,
                        leaserSchoolYear,
                        leaserMajor,
                        leaserEmail,
                        leaserPhone,
                        profilePhoto,
                        leaserIntro,
                        roomId,
                        negotiable,
                      };
                      if (favorites && favorites[roomId]) {
                        // need to remove from the favorites
                        dispatch(removeHousingFavorite(roomId));
                      } else {
                        // need to add to the favorites
                        dispatch(newHousingFavorite(housePost));
                      }
                    }}
                  >
                    {favorites && favorites[roomId] ? '-' : '+'}
                  </Button>
                </Col>
                <Col xs={{ span: 3, offset: 1 }}>
                  <Button variant="no-show">
                    <contactIcons.share />
                  </Button>
                </Col>
              </Row>

              <div className="address-related-text">
                <b>~ {distance}</b>&nbsp;public transit
              </div>
              <div className="secondary-text">
                {abbreviateAddress(location)}
              </div>
              <GoogleMap address={location} className="house-profile-map" />
            </div>

            <Container className="housing-profile-bio">
              <Row>
                <Col xs={8} lg={9} className="text-center">
                  <div className="primary-text">{leaserName}</div>

                  <div className="secondary-text">
                    {leaserSchoolYear} | {leaserMajor}
                  </div>

                  <Row className="justify-content-center">
                    <OverlayTrigger
                      placement="bottom"
                      overlay={
                        <Tooltip id="tooltip">
                          {user ? leaserEmail : LOGIN_TO_VIEW}
                        </Tooltip>
                      }
                    >
                      <contactIcons.email
                        className="d-block mr-3"
                        onClick={async () => {
                          if (user) {
                            await navigator.clipboard.writeText(leaserEmail);
                            window.open(`mailto:${leaserEmail}`, '_blank');
                          }
                        }}
                      />
                    </OverlayTrigger>

                    <OverlayTrigger
                      placement="bottom"
                      overlay={
                        <Tooltip id="tooltip">
                          {user ? leaserPhone : LOGIN_TO_VIEW}
                        </Tooltip>
                      }
                    >
                      <contactIcons.phone
                        className="d-block mr-3"
                        onClick={async () => {
                          if (user) {
                            await navigator.clipboard.writeText(leaserPhone);
                            window.open(`tel:${leaserPhone}`, '_blank');
                          }
                        }}
                      />
                    </OverlayTrigger>
                  </Row>
                </Col>

                <Col xs={4} lg={3} className="mt-auto text-center">
                  <Image src={profilePhoto} roundedCircle className="w-100" />
                </Col>
              </Row>

              <div className="housing-profile-speech-bubble">{leaserIntro}</div>
            </Container>
          </Col>
        </Row>
      </Container>
    </Modal>
  );
};

export default HouseProfile;
