CREATE TABLE channel_module (
    channel_id uuid NOT NULL,
    module character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT channel_module_channel_id_key UNIQUE (channel_id)
)
WITH (
    OIDS = FALSE)
TABLESPACE pg_default;

INSERT INTO channel_module
SELECT
    id AS channel_id,
    'numeracy' AS module
FROM
    content_channelmetadata;

