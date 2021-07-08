import React, { FunctionComponent } from 'react';
import styles from './FilledImage.module.scss';
import cn from 'classnames';

interface Props
  extends React.DetailedHTMLProps<
    React.HTMLAttributes<HTMLDivElement>,
    HTMLDivElement
  > {
  src: string;
  alt?: string;
}

const FilledImage: FunctionComponent<Props> = ({
  src,
  alt,
  className,
  style,
  ...divProps
}) => {
  return (
    <div className={styles.wrapper}>
      <div
        {...divProps}
        className={cn(styles.image, className)}
        style={{ backgroundImage: `url("${src}")`, ...style }}
      >
        <img src="NA" className={styles.hiddenImage} alt={alt} />
      </div>
    </div>
  );
};

export default FilledImage;
