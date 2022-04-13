# Load libraries
library(purrr)
library(DBI)
library(RPostgreSQL)
library(dplyr)
library(dbplyr)
library(pool)

# Create a pool connection to the local Kolibri database
kol_pool <- dbPool(
  drv = RPostgreSQL::PostgreSQL(),
  dbname = Sys.getenv("KOLIBRI_DATABASE_NAME"),
  host = Sys.getenv("KOLIBRI_DATABASE_HOST"),
  user = Sys.getenv("KOLIBRI_DATABASE_USER"),
  password = Sys.getenv("KOLIBRI_DATABASE_PASSWORD"),
  port = Sys.getenv("KOLIBRI_DATABASE_PORT")
)

# get channel metadata
channel_meta <- kol_pool %>%
  dplyr::tbl("content_channelmetadata") %>%
  dplyr::collect()

# get contentnodes
contentnodes <- kol_pool %>%
  dplyr::tbl("content_contentnode") %>%
  dplyr::collect()

# function to generate pairs of prerequisites by channel
generate_prereqs_by_channel <- function(channel) {
  # get all contentnodes belonging to the inputted channel
  # order by lft
  # get the ids as an atomic vector
  nodes_sort_order <- contentnodes %>%
    dplyr::filter(channel_id == channel, kind != "topic", parent_id != channel_id) %>%
    dplyr::arrange(lft) %>%
    dplyr::pull(id)
  # derive vectors of to_contentnode_id and from_contentnode_id using lead and lag
  to_c <- lag(nodes_sort_order)
  from_c <- lead(nodes_sort_order)

  # drop the na at the top and bottom for to and from respectively
  to_c <- to_c[!is.na(to_c)]
  from_c <- from_c[!is.na(from_c)]

  # convert the result to a dataframe with column names to match the kolibri db
  prereqs_vec <- data.frame(from_contentnode_id = from_c, to_contentnode_id = to_c)

  # return the prerequisites dataframe
  return(prereqs_vec)
}

# channel ids for coach professional development
coach_content <- c("2c8cd5f3-a469-4adb-b4be-45025d9ca3dc", "19ea4c94-ee48-4cb0-b5bb-617f5511f4c1")

# get wanted channel ids as atomic vector
channel_ids <- channel_meta %>%
  dplyr::filter(!id %in% coach_content) %>%
  dplyr::pull(id)

# Walk through the wanted channel_ids and generate the prerequisites
# Bind all of the results into a single dataframe
all_prereqs <- channel_ids %>%
  purrr::map(generate_prereqs_by_channel) %>%
  purrr::map_dfr(rbind)

# delete all existing prerequisites
dbGetQuery(kol_pool, "delete from content_contentnode_has_prerequisite")
print("Deleting existing prerequisites")

print("Inserting prerequisites")
# Write the derived prerequisites to the local Kolibri database
dbWriteTable(kol_pool, "content_contentnode_has_prerequisite", all_prereqs, row.names = FALSE, append = TRUE)
print("Done")

poolClose(kol_pool)