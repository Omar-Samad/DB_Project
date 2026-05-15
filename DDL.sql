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