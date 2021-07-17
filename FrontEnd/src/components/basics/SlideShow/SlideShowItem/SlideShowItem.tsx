import React, { FunctionComponent } from 'react';
import { CarouselItem, CarouselItemProps } from 'reactstrap';
import cn from 'classnames';
import { FilledImage } from '@basics';
import styles from './SlideShowItem.module.scss';

interface SlideShowItemProps extends CarouselItemProps {
  src: string;
  alt: string;
  onClick?: () => any;
}

const SlideShowItem: FunctionComponent<SlideShowItemProps> = ({
  src,
  alt,
  onClick,
  className,
  ...carouselItemProps
}) => {
  const imageElement = <FilledImage src={src} alt={alt} />; // Will be reused in two spots below

  return (
    <CarouselItem
      {...carouselItemProps}
      key={src}
      className={cn(styles.item, className)}
    >
      {onClick ? (
        <div
          className={styles.wrapper}
          onClick={onClick}
          onKeyDown={({ key }) => key === 'Enter' && onClick()}
        >
          {imageElement}
        </div>
      ) : (
        imageElement
      )}
    </CarouselItem>
  );
};

export default SlideShowItem;
