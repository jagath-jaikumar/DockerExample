CREATE DATABASE content;
use content;

CREATE TABLE images (
  uuid VARCHAR(36),
  image TEXT(65535)
);

INSERT INTO images
  (uuid, image)
VALUES
  ('sample_ID', 'sample_image');
