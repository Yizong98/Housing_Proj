import React, { FunctionComponent } from 'react';
import { SlideShowItem } from '../SlideShow';
import styles from './Thumbnails.module.scss';
import cn from 'classnames';
import { FilledImage } from '@basics';

interface ThumbnailProps
  extends React.DetailedHTMLProps<
    React.HTMLAttributes<HTMLDivElement>,
    HTMLDivElement
  > {
  image: SlideShowItem;
  active?: boolean;
}

const Thumbnail: FunctionComponent<ThumbnailProps> = ({
  image,
  active,
  className,
  ...divProps
}) => (
  <div
    {...divProps}
    className={cn(
      className,
      {
        [styles.selectedPreview]: !active,
      },
      styles.clickable,
    )}
  >
    <FilledImage src={image.src} alt={image.alt} />
  </div>
);

export default Thumbnail;
