library(RSQLite)
library(dplyr)

conn <- dbConnect(SQLite(), 'chucks.db')
raw_data <- dbGetQuery(conn, "SELECT * FROM Beerlist")
dbDisconnect(conn)

key_metrics <- 
  raw_data %>% 
  mutate(pint_cost = as.numeric(substring(pint_cost,2)),
         abv = as.numeric(abv),
         print_label = paste(brewery, beer, sep=":")) %>%
  select(brewery, beer, pint_cost, growler_cost, abv, print_label) %>%
  distinct

lengths <-
  raw_data %>%
  mutate(datetime = as.POSIXct(datetime),
         day = lubridate::day(datetime)) %>%
  subset(datetime >= as.POSIXct("2016-01-29 11:00:00")) %>%
  group_by(day, brewery, beer) %>%
  do(data.frame(earliest = min(.$datetime),
     latest = max(.$datetime))) %>%
  mutate(pour_time = difftime(latest, earliest, units="secs")) %>%
  ungroup() %>%
  group_by(brewery, beer) %>%
  do(data.frame(total = sum(.$pour_time),
                totaldays = length(unique(.$day)))) %>%
  mutate(on_tap = (total/totaldays) / 60)

for_plot <-
  key_metrics %>%
  select(pint_cost, abv, print_label) %>%
  distinct

p <- ggplot(for_plot, aes(x=abv, y=pint_cost, label = print_label))
p + geom_text(check_overlap = TRUE)
ggsave("cost_vs_abv.png")

lengths_metrics <- merge(lengths, key_metrics)

p <- ggplot(lengths_metrics, aes(x=abv, y=on_tap, label = print_label))
p + geom_text(check_overlap = TRUE) + 
  ggtitle("Minutes on tap vs. ABV per pint")
ggsave("min_on_tap_vs_abv.png")

p <- ggplot(lengths_metrics, aes(x=pint_cost, y=on_tap, label = print_label))
p + geom_text(check_overlap = TRUE) +
  ggtitle("Minutes on tap vs. price per pint")
ggsave("min_on_tap_vs_price.png")