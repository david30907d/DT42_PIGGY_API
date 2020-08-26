CALL CREATE_ODS_FARM_ID_TIMESTAMP();

INSERT INTO
    ODS_FARM_ID_TIMESTAMP (
        COMPRESSION,
        IMAGE_BLOB,
        CHANNEL,
        TIMESTAMP,
        ANNOTATIONS
    )
VALUES
    (
        'jpeg',
        DECODE('DEADBEEF', 'hex'),
        0,
        CURRENT_TIMESTAMP,
        '[
        {
           "type": "detection",
           "label": "person",
           "confidence": 0.93,
           "top": 100,
           "bottom": 200,
           "left": 50,
           "right": 128
        }]'
    ),
    (
        'jpeg',
        DECODE('DEADBEEF', 'hex'),
        0,
        CURRENT_TIMESTAMP,
        '[
        {
           "type": "detection",
           "label": "person",
           "confidence": 0.93,
           "top": 100,
           "bottom": 200,
           "left": 50,
           "right": 128
        }]'
    ),
    (
        'jpeg',
        DECODE('DEADBEEF', 'hex'),
        0,
        CURRENT_TIMESTAMP,
        '[
        {
           "type": "detection",
           "label": "person",
           "confidence": 0.93,
           "top": 100,
           "bottom": 200,
           "left": 50,
           "right": 128
        }]'
    );