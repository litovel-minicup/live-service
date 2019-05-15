# Litovel MINICUP - livestream service

Tornado server used for distributing live results from matches - all database changes are performed via Django models of MINICUP defined in `litovel-minicup-model` package.

# API
## Standard types
### MatchEvent
```javascript
{
  id: 42,
  half_index: 1, // 0/1 for first/second half
  time_offset: 38, // seconds after start of current half
  message: "Player one scored",
  score: [12, 10],
  type: "goal", // one of start,goald,end,info
  team_index: 1, // -1 if not related to team
  absolute_time: 1447585410450, // standard unix timestamp
  match_id: 368,
  team_id: 25, // null if not related
  
  // null if not related to player
  player_id: 85,
  player_name: "Son Hai Nguyen",
  player_number: 25,
}
```
### Player
```javascript
{
      id: 42,
      name: "Son Hai Nguyen",
      number: 68,
      firstname: "Son",
      lastname: "Hai Nguyen"
}
```
### Team
```javascript
{
      id: 42,
      trainer_name: "Son Hai Nguyen",
      name: "Team Foo",
      dress_color: "red",
}
```

## Static REST

### `GET /api/category-list`
Returns all categories with unconfirmed matches.
```javascript
{
  categories: [
    {id: 42, name: "Mladší"},
    ...
  ]
}
```

### `GET /api/category/<ID>`
Returns all unconfirmed matches in category (in case of non existing unconfirmed returns all matches in category).
```javascript
{
  matches: [
    {
      id: 42,
      name: "A vs. B",
      date: "15:00 1.1.2020",
      location: "A",
      state: "init", // one of [init, half_first, pause, half_second, end]
    },
    ...
  ]
}
```

### `GET /api/match/<ID>`
Returns player rosters for match.
```javascript
{
  home_team_players: [Player, ...],
  away_team_players: [Player, ...],
}
```

### `GET /api/match-events/<ID>`
Returns all events for match, sorted asc by time.
```javascript
{
  events: [MatchEvent, MatchEvent, ...]
}
```

### `GET /api/team-detail/<ID>`
Returns more details for team.
```javascript
{
  **Team,
  points: 25,
  order: 1,
  scored: 25,
  received: 85,
  description: "Team trained by ..., good pre-season results....",
  players: [{**Player, total_goals: 25}, ...],
  matches: [Match, Match, ....]
}
```

