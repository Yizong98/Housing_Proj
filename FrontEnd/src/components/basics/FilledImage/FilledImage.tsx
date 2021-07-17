import React, { FunctionComponent } from 'react';
import styles from './FilledImage.module.scss';
import cn from 'classnames';

interface FilledImageProps
  extends React.DetailedHTMLProps<
    React.HTMLAttributes<HTMLDivElement>,
    HTMLDivElement
  > {
  src: string;
  alt?: string;
}

/**
 * FilledImage uses the `src` prop provided as the `background-image`
 * of a `div` with `background-size: cover;`. This simulates
 * an image that fills the provided height/width without
 * stretching.
 *
 * It also provides a hidden image with the same `src` and provided `alt`
 * for any browser/scraping/accessibility reasons.
 */
const FilledImage: FunctionComponent<FilledImageProps> = ({
  src,
  alt,
  className,
  style,
  ...divProps
}) => (
  <div
    {...divProps}
    className={cn(styles.image, className)}
    style={{ backgroundImage: `url("${src}")`, ...style }}
  >
    <img src="NA" className={styles.hiddenImage} alt={alt} />
  </div>
);

export default FilledImage;
