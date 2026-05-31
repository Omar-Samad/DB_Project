CREATE DATABASE IF NOT EXISTS lost_and_found;
USE lost_and_found;
CREATE INDEX idx_lost_user ON lost_items(user_id);
CREATE INDEX idx_lost_category ON lost_items(category_id);
CREATE INDEX idx_lost_status ON lost_items(status);
CREATE INDEX idx_lost_location ON lost_items(location);

CREATE INDEX idx_found_user ON found_items(user_id);
CREATE INDEX idx_found_category ON found_items(category_id);
CREATE INDEX idx_found_status ON found_items(status);
CREATE INDEX idx_found_expiry ON found_items(expiry_date);
CREATE INDEX idx_found_location ON found_items(location);

CREATE INDEX idx_match_lost ON matches(lost_id);
CREATE INDEX idx_match_found ON matches(found_id);
CREATE INDEX idx_match_status ON matches(match_status);

CREATE INDEX idx_claim_item on claims(item_id);
create index idx_claim_user on claims(user_id);
create INDEX idx_claim_status ON claims(status);

CREATE INDEX idx_notif_user on notifications(user_id);

