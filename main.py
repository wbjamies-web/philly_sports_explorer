"""
Philly Sports History Explorer
Bruce Jamieson - CS1 Final Project

This website lets someone explore Philadelphia sports history in one place.
The user picks a team, a decade, and a few other filters, and the site shows
the important events that match. The user can also save their favorite
moments and add their own events to the timeline.
"""

from drafter import *
from bakery import assert_equal
from dataclasses import dataclass


set_site_information(
    author="wbjamies@udel.edu (Bruce Jamieson)",
    description="""Philly Sports History Explorer lets fans explore the
    history of the Phillies, Eagles, 76ers, and Flyers in one place.
    You can filter events by team, decade, and championships, save your
    favorite moments, and add your own events to the timeline.""",
    sources=[
        "Official Drafter documentation: "
        "https://drafter-edu.github.io/drafter/",
        "Claude (LLM) helped me write and debug the code. The full "
        "conversation is uploaded in this repository."
    ],
    planning=["pick_a_problem.docx", "design.docx"],
    links=["github_link",
           "youtube_video"]
)
hide_debug_information()
set_website_title("Philly Sports History Explorer")
set_website_framed(False)


# Global constants (these never change while the site is running)
ALL_TEAMS = "All Teams"
ALL_DECADES = "All Decades"
TEAM_NAMES = ["Phillies", "Eagles", "76ers", "Flyers"]
TEAM_OPTIONS = [ALL_TEAMS] + TEAM_NAMES
DECADE_OPTIONS = [ALL_DECADES, "1880s", "1890s", "1900s", "1910s", "1920s",
                  "1930s", "1940s", "1950s", "1960s", "1970s", "1980s",
                  "1990s", "2000s", "2010s", "2020s"]
EARLIEST_YEAR = 1850
LATEST_YEAR = 2030
NO_EVENTS_MESSAGE = "No events found. Try changing your filters."
NO_FAVORITES_MESSAGE = "You have not saved any moments yet."


@dataclass
class Event:
    """One moment in Philadelphia sports history."""
    name: str
    year: int
    team: str
    description: str
    is_championship: bool
    is_favorite: bool


@dataclass
class State:
    """Everything the website needs to remember between pages."""
    events: list[Event]
    selected_team: str
    selected_decade: str
    championships_only: bool
    search_word: str


def make_starting_events() -> list[Event]:
    """Create the list of events the website starts with, oldest first."""
    return [
        Event("Phillies Play Their First Season", 1883, "Phillies",
              "Philadelphia's National League baseball team played its "
              "first season in 1883. It is one of the oldest teams in "
              "all of American professional sports.", False, False),
        Event("First National League Pennant", 1915, "Phillies",
              "Behind pitcher Grover Cleveland Alexander, the Phillies won "
              "their first pennant. They lost the World Series to the "
              "Boston Red Sox.", False, False),
        Event("The Eagles Are Founded", 1933, "Eagles",
              "Bert Bell and Lud Wray started the Philadelphia Eagles in "
              "1933. The team was named after the eagle symbol of the "
              "National Recovery Administration.", False, False),
        Event("First NFL Championship", 1948, "Eagles",
              "The Eagles beat the Chicago Cardinals 7-0 in a snowstorm at "
              "Shibe Park. Steve Van Buren scored the only touchdown of "
              "the game.", True, False),
        Event("Back to Back NFL Champions", 1949, "Eagles",
              "The Eagles shut out the Los Angeles Rams 14-0 in the rain "
              "to win their second NFL title in a row.", True, False),
        Event("The Whiz Kids Win the Pennant", 1950, "Phillies",
              "A young Phillies team nicknamed the Whiz Kids won the "
              "National League pennant on the last day of the season. "
              "They lost the World Series to the Yankees.", False, False),
        Event("Champions at Franklin Field", 1960, "Eagles",
              "The Eagles beat the Green Bay Packers 17-13 for the NFL "
              "Championship. Chuck Bednarik made the final tackle to "
              "save the game.", True, False),
        Event("The 76ers Come to Philadelphia", 1963, "76ers",
              "The Syracuse Nationals moved to Philadelphia and were "
              "renamed the 76ers, after the year 1776 when the "
              "Declaration of Independence was signed here.", False, False),
        Event("Jim Bunning's Perfect Game", 1964, "Phillies",
              "Jim Bunning threw a perfect game against the New York Mets "
              "on Father's Day. No Mets batter reached base.", False, False),
        Event("76ers Win the NBA Title", 1967, "76ers",
              "Led by Wilt Chamberlain, the 76ers won 68 games and beat "
              "the San Francisco Warriors in the NBA Finals.", True, False),
        Event("The Flyers Take the Ice", 1967, "Flyers",
              "The Flyers played their first season as one of six new "
              "teams added to the NHL in 1967.", False, False),
        Event("First Stanley Cup", 1974, "Flyers",
              "The Broad Street Bullies beat the Boston Bruins to become "
              "the first expansion team to win the Stanley Cup. Bernie "
              "Parent was the playoff MVP.", True, False),
        Event("Second Stanley Cup in a Row", 1975, "Flyers",
              "The Flyers beat the Buffalo Sabres in six games to win the "
              "Stanley Cup for the second year in a row.", True, False),
        Event("Flyers Beat the Soviet Red Army", 1976, "Flyers",
              "The Flyers beat the Soviet Red Army team 4-1 at the "
              "Spectrum. They were the only NHL team to beat them on "
              "that tour.", False, False),
        Event("First World Series Title", 1980, "Phillies",
              "After almost 100 years, the Phillies finally won the World "
              "Series by beating the Kansas City Royals in six games. Tug "
              "McGraw got the final strikeout.", True, False),
        Event("First Super Bowl Appearance", 1981, "Eagles",
              "Coach Dick Vermeil took the Eagles to Super Bowl XV, their "
              "first Super Bowl. They lost to the Oakland Raiders 27-10.",
              False, False),
        Event("76ers Sweep the Lakers", 1983, "76ers",
              "With Moses Malone and Julius Erving, the 76ers lost only "
              "one playoff game and swept the Lakers in the NBA Finals.",
              True, False),
        Event("Worst to First Pennant", 1993, "Phillies",
              "The Phillies went from last place to the World Series in "
              "one year. They lost to the Toronto Blue Jays on Joe "
              "Carter's home run.", False, False),
        Event("Iverson Leads 76ers to the Finals", 2001, "76ers",
              "Allen Iverson won the MVP award and carried the 76ers to "
              "the NBA Finals. They won Game 1 but lost the series to the "
              "Lakers.", False, False),
        Event("Super Bowl XXXIX", 2005, "Eagles",
              "Donovan McNabb and the Eagles reached the Super Bowl after "
              "three straight losses in the NFC Championship. They lost "
              "to the New England Patriots 24-21.", False, False),
        Event("World Champions Again", 2008, "Phillies",
              "The Phillies beat the Tampa Bay Rays in five games to win "
              "their second World Series. Brad Lidge got the last out to "
              "finish a perfect season as closer.", True, False),
        Event("Roy Halladay's Perfect Game", 2010, "Phillies",
              "Roy Halladay threw a perfect game in May, and then threw a "
              "no-hitter in his first playoff start that October.",
              False, False),
        Event("Comeback from Down 3-0", 2010, "Flyers",
              "The Flyers came back from being down three games to none "
              "against the Bruins and made it all the way to the Stanley "
              "Cup Final.", False, False),
        Event("First Super Bowl Win", 2018, "Eagles",
              "The Eagles beat the Patriots 41-33 in Super Bowl LII. "
              "Backup quarterback Nick Foles was the MVP and caught a "
              "touchdown on the Philly Special.", True, False),
        Event("Red October", 2022, "Phillies",
              "The Phillies got into the playoffs as the last wild card "
              "team and went all the way to the World Series. They lost "
              "to the Houston Astros in six games.", False, False),
        Event("Super Bowl LVII", 2023, "Eagles",
              "Jalen Hurts scored four touchdowns, but the Eagles lost to "
              "the Kansas City Chiefs 38-35 on a late field goal.",
              False, False),
        Event("Second Super Bowl Win", 2025, "Eagles",
              "The Eagles beat the Chiefs 40-22 in Super Bowl LIX and "
              "stopped Kansas City from winning three in a row. Jalen "
              "Hurts was the MVP.", True, False)
    ]


def make_starting_state() -> State:
    """Create the State the website has when it first opens."""
    return State(make_starting_events(), ALL_TEAMS, ALL_DECADES, False, "")


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def get_decade(year: int) -> str:
    """Turn a year like 1983 into the name of its decade, like '1980s'."""
    return str(year // 10 * 10) + "s"


def matches_team(event: Event, selected_team: str) -> bool:
    """Decide if an event belongs to the team the user picked."""
    if selected_team == ALL_TEAMS:
        return True
    return event.team == selected_team


def matches_decade(event: Event, selected_decade: str) -> bool:
    """Decide if an event happened in the decade the user picked."""
    if selected_decade == ALL_DECADES:
        return True
    return get_decade(event.year) == selected_decade


def matches_search(event: Event, search_word: str) -> bool:
    """Decide if the search word is in the event's name or description."""
    cleaned_word = search_word.strip().lower()
    if cleaned_word == "":
        return True
    in_name = cleaned_word in event.name.lower()
    in_description = cleaned_word in event.description.lower()
    return in_name or in_description


def event_matches_filters(event: Event, state: State) -> bool:
    """Decide if an event passes every filter the user has chosen."""
    if state.championships_only and not event.is_championship:
        return False
    return (matches_team(event, state.selected_team) and
            matches_decade(event, state.selected_decade) and
            matches_search(event, state.search_word))


def find_matching_positions(state: State) -> list[int]:
    """
    Loop through every event and collect the positions (indexes) of the
    ones that match the user's filters. I save positions instead of the
    events so that the buttons can tell the details page which event
    was clicked.
    """
    matching_positions = []
    position = 0
    for event in state.events:
        if event_matches_filters(event, state):
            matching_positions.append(position)
        position = position + 1
    return matching_positions


def count_championships(events: list[Event], team: str) -> int:
    """Count how many championship events a team has."""
    championship_count = 0
    for event in events:
        if event.team == team and event.is_championship:
            championship_count = championship_count + 1
    return championship_count


def count_favorites(events: list[Event]) -> int:
    """Count how many events the user has saved as favorites."""
    favorite_count = 0
    for event in events:
        if event.is_favorite:
            favorite_count = favorite_count + 1
    return favorite_count


def is_valid_year(year_text: str) -> bool:
    """Decide if the text the user typed is a year the site can use."""
    cleaned_text = year_text.strip()
    if not cleaned_text.isdigit():
        return False
    year = int(cleaned_text)
    return EARLIEST_YEAR <= year and year <= LATEST_YEAR


def is_valid_position(events: list[Event], position: int) -> bool:
    """Decide if a position is a real index in the list of events."""
    return 0 <= position and position < len(events)


def find_insert_position(events: list[Event], year: int) -> int:
    """
    Find where a new event should go so the list stays in order by year.
    The new event goes after any events from the same year.
    """
    insert_position = 0
    for event in events:
        if event.year <= year:
            insert_position = insert_position + 1
    return insert_position


def get_team_color(team: str) -> str:
    """Give back the main color of a Philadelphia team."""
    if team == "Phillies":
        return "crimson"
    elif team == "Eagles":
        return "darkgreen"
    elif team == "76ers":
        return "royalblue"
    elif team == "Flyers":
        return "darkorange"
    return "black"


def describe_filters(state: State) -> str:
    """Make a sentence that tells the user which filters are turned on."""
    summary = "Team: " + state.selected_team
    summary = summary + " | Decade: " + state.selected_decade
    if state.championships_only:
        summary = summary + " | Championships only"
    if state.search_word.strip() != "":
        summary = summary + " | Search: " + state.search_word.strip()
    return summary


def make_event_label(event: Event) -> str:
    """Make the short text shown next to an event in a list."""
    label = str(event.year) + " - " + event.team + " - "
    if event.is_championship:
        label = label + "(Champions) "
    if event.is_favorite:
        label = label + "(Saved) "
    return label


def make_event_row(event: Event, position: int) -> Div:
    """
    Make one row for an event with a button that opens its details.
    The Argument sends the event's position to the event_details route
    without the user having to type anything.
    """
    return Div(
        change_color(bold(make_event_label(event)),
                     get_team_color(event.team)),
        Button(event.name, event_details,
               [Argument("event_position", position)])
    )


def make_navigation() -> Div:
    """Make the row of buttons that is shown at the bottom of pages."""
    return Div(
        Button("Home", index),
        Button("Explore Events", choose_team),
        Button("Championships", championships_page),
        Button("My Saved Moments", favorites_page),
        Button("Add an Event", add_event_page)
    )


def make_message_page(state: State, title: str, message: str) -> Page:
    """Make a simple page that only shows a title and a message."""
    return Page(state, [
        Header(title),
        message,
        HorizontalRule(),
        make_navigation()
    ])


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

@route
def index(state: State) -> Page:
    """Show the home page with the title and the main buttons."""
    event_total = len(state.events)
    saved_total = count_favorites(state.events)
    return Page(state, [
        Header("Philly Sports History Explorer"),
        Div("Explore more than a century of Philadelphia sports history "
            "in one place. Pick a team and a decade to see the moments "
            "that matter."),
        Div(bold("Events in the timeline: " + str(event_total))),
        Div(bold("Moments you have saved: " + str(saved_total))),
        HorizontalRule(),
        Div(
            Button("Start Exploring", choose_team),
            Button("View Championships", championships_page),
            Button("My Saved Moments", favorites_page)
        ),
        Div(
            Button("Add an Event", add_event_page),
            Button("About This Site", about_page)
        )
    ])


@route
def choose_team(state: State) -> Page:
    """Show the page where the user picks a team."""
    return Page(state, [
        Header("Step 1: Choose a Team"),
        Div("Which team do you want to explore?"),
        SelectBox("team_choice", TEAM_OPTIONS, state.selected_team),
        LineBreak(),
        Button("Next", set_team),
        HorizontalRule(),
        make_navigation()
    ])


@route
def set_team(state: State, team_choice: str) -> Page:
    """Save the team the user picked and move on to the filters page."""
    if team_choice in TEAM_OPTIONS:
        state.selected_team = team_choice
    else:
        state.selected_team = ALL_TEAMS
    return choose_decade(state)


@route
def choose_decade(state: State) -> Page:
    """Show the page where the user picks a decade and other filters."""
    return Page(state, [
        Header("Step 2: Choose Your Filters"),
        Div("Team: ", change_color(bold(state.selected_team),
                                   get_team_color(state.selected_team))),
        Div("Decade:"),
        SelectBox("decade_choice", DECADE_OPTIONS, state.selected_decade),
        LineBreak(),
        CheckBox("championships_choice", state.championships_only),
        "Championships only",
        LineBreak(),
        Div("Search for a word (optional), like a player's name:"),
        TextBox("search_choice", state.search_word),
        LineBreak(),
        Button("Show Events", set_filters),
        Button("Change Team", choose_team),
        HorizontalRule(),
        make_navigation()
    ])


@route
def set_filters(state: State, decade_choice: str,
                championships_choice: bool, search_choice: str) -> Page:
    """Save the decade, checkbox, and search word, then show the results."""
    if decade_choice in DECADE_OPTIONS:
        state.selected_decade = decade_choice
    else:
        state.selected_decade = ALL_DECADES
    state.championships_only = championships_choice
    state.search_word = search_choice.strip()
    return show_events(state)


@route
def clear_filters(state: State) -> Page:
    """Reset every filter back to how it started and show all events."""
    state.selected_team = ALL_TEAMS
    state.selected_decade = ALL_DECADES
    state.championships_only = False
    state.search_word = ""
    return show_events(state)


@route
def show_events(state: State) -> Page:
    """Show every event that matches the filters the user picked."""
    matching_positions = find_matching_positions(state)
    content = [
        Header("Matching Events"),
        Div(italic(describe_filters(state))),
        HorizontalRule()
    ]
    if len(matching_positions) == 0:
        content.append(NO_EVENTS_MESSAGE)
    else:
        content.append(Div("Found " + str(len(matching_positions)) +
                           " event(s). Click one to read more."))
        for position in matching_positions:
            content.append(make_event_row(state.events[position], position))
    content.append(HorizontalRule())
    content.append(Div(Button("Change Filters", choose_decade),
                       Button("Clear Filters", clear_filters)))
    content.append(make_navigation())
    return Page(state, content)


@route
def event_details(state: State, event_position: int) -> Page:
    """Show all of the information about one event."""
    if not is_valid_position(state.events, event_position):
        return make_message_page(state, "Event Not Found",
                                 "Sorry, that event does not exist.")
    event = state.events[event_position]
    if event.is_championship:
        championship_text = "Yes, this was a championship!"
    else:
        championship_text = "No"
    if event.is_favorite:
        favorite_button_text = "Remove from My Saved Moments"
    else:
        favorite_button_text = "Save to My Saved Moments"
    return Page(state, [
        change_color(Header(event.name), get_team_color(event.team)),
        Div(bold("Year: "), str(event.year)),
        Div(bold("Team: "), event.team),
        Div(bold("Championship: "), championship_text),
        Div(bold("What happened: "), event.description),
        HorizontalRule(),
        Div(
            Button(favorite_button_text, toggle_favorite,
                   [Argument("event_position", event_position)]),
            Button("Back to Results", show_events)
        ),
        make_navigation()
    ])


@route
def toggle_favorite(state: State, event_position: int) -> Page:
    """Save an event as a favorite, or remove it if it was already saved."""
    if is_valid_position(state.events, event_position):
        event = state.events[event_position]
        if event.is_favorite:
            event.is_favorite = False
        else:
            event.is_favorite = True
    return event_details(state, event_position)


@route
def favorites_page(state: State) -> Page:
    """Show all of the events the user has saved."""
    content = [
        Header("My Saved Moments"),
        Div("These are the moments you saved while exploring."),
        HorizontalRule()
    ]
    position = 0
    for event in state.events:
        if event.is_favorite:
            content.append(make_event_row(event, position))
        position = position + 1
    if count_favorites(state.events) == 0:
        content.append(NO_FAVORITES_MESSAGE)
    content.append(HorizontalRule())
    content.append(make_navigation())
    return Page(state, content)


@route
def championships_page(state: State) -> Page:
    """Show how many titles each team has and list every championship."""
    title_table = [["Team", "Championships"]]
    for team in TEAM_NAMES:
        title_count = count_championships(state.events, team)
        title_table.append([team, str(title_count)])
    content = [
        Header("Philadelphia Championships"),
        Table(title_table),
        Header("Every Title", 3)
    ]
    position = 0
    for event in state.events:
        if event.is_championship:
            content.append(make_event_row(event, position))
        position = position + 1
    content.append(HorizontalRule())
    content.append(make_navigation())
    return Page(state, content)


@route
def add_event_page(state: State) -> Page:
    """Show the form that lets the user add their own event."""
    return Page(state, [
        Header("Add Your Own Event"),
        Div("Is there a Philly sports moment that is missing? Add it to "
            "the timeline here."),
        Div("Event name:"),
        TextBox("new_name"),
        Div("Year:"),
        TextBox("new_year"),
        Div("Team:"),
        SelectBox("new_team", TEAM_NAMES),
        Div("What happened:"),
        TextArea("new_description"),
        LineBreak(),
        CheckBox("new_is_championship"),
        "This was a championship",
        LineBreak(),
        Button("Add Event", save_new_event),
        HorizontalRule(),
        make_navigation()
    ])


@route
def save_new_event(state: State, new_name: str, new_year: str,
                   new_team: str, new_description: str,
                   new_is_championship: bool) -> Page:
    """Check the form, and if it is filled in right, add the new event."""
    if new_name.strip() == "":
        return make_message_page(state, "Event Not Added",
                                 "Please go back and give the event a name.")
    if not is_valid_year(new_year):
        return make_message_page(
            state, "Event Not Added",
            "Please go back and type a year between " + str(EARLIEST_YEAR) +
            " and " + str(LATEST_YEAR) + ".")
    if new_team not in TEAM_NAMES:
        return make_message_page(state, "Event Not Added",
                                 "Please go back and pick a team.")
    year = int(new_year.strip())
    new_event = Event(new_name.strip(), year, new_team,
                      new_description.strip(), new_is_championship, False)
    insert_position = find_insert_position(state.events, year)
    state.events.insert(insert_position, new_event)
    return event_details(state, insert_position)


@route
def about_page(state: State) -> Page:
    """Show information about the website and how to use it."""
    return Page(state, [
        Header("About This Site"),
        Div("Philadelphia has a long sports history, but the information "
            "is spread out across a lot of different websites. Philly "
            "Sports History Explorer puts the biggest moments from the "
            "Phillies, Eagles, 76ers, and Flyers in one place."),
        Header("How to Use It", 3),
        BulletedList([
            "Click Start Exploring and pick a team.",
            "Pick a decade, check the box if you only want championships, "
            "or type a word to search for.",
            "Click an event to read what happened.",
            "Save the moments you like and find them in My Saved Moments.",
            "Add your own event if something is missing."
        ]),
        Div(italic("Note: Super Bowls are listed under the year the game "
                   "was actually played.")),
        HorizontalRule(),
        make_navigation()
    ])


# ---------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------

def make_test_events() -> list[Event]:
    """Create a small list of events that is only used by the tests."""
    return [
        Event("First Stanley Cup", 1974, "Flyers", "Beat the Bruins.",
              True, False),
        Event("First World Series Title", 1980, "Phillies",
              "Tug McGraw got the last out.", True, False),
        Event("First Super Bowl Appearance", 1981, "Eagles",
              "Lost to the Raiders.", False, False)
    ]


def make_test_state() -> State:
    """Create a small State that is only used by the tests."""
    return State(make_test_events(), ALL_TEAMS, ALL_DECADES, False, "")


# Tests for the helper functions
assert_equal(get_decade(1983), "1980s")
assert_equal(get_decade(2008), "2000s")
assert_equal(get_decade(1960), "1960s")

assert_equal(matches_team(make_test_events()[0], ALL_TEAMS), True)
assert_equal(matches_team(make_test_events()[0], "Flyers"), True)
assert_equal(matches_team(make_test_events()[0], "Eagles"), False)

assert_equal(matches_decade(make_test_events()[1], ALL_DECADES), True)
assert_equal(matches_decade(make_test_events()[1], "1980s"), True)
assert_equal(matches_decade(make_test_events()[1], "1970s"), False)

assert_equal(matches_search(make_test_events()[1], ""), True)
assert_equal(matches_search(make_test_events()[1], "  MCGRAW "), True)
assert_equal(matches_search(make_test_events()[1], "world series"), True)
assert_equal(matches_search(make_test_events()[1], "hockey"), False)

assert_equal(event_matches_filters(make_test_events()[2],
                                   make_test_state()), True)
assert_equal(event_matches_filters(
    make_test_events()[2],
    State(make_test_events(), ALL_TEAMS, ALL_DECADES, True, "")), False)
assert_equal(event_matches_filters(
    make_test_events()[1],
    State(make_test_events(), "Phillies", "1980s", True, "tug")), True)

assert_equal(find_matching_positions(make_test_state()), [0, 1, 2])
assert_equal(find_matching_positions(
    State(make_test_events(), "Eagles", ALL_DECADES, False, "")), [2])
assert_equal(find_matching_positions(
    State(make_test_events(), ALL_TEAMS, "1980s", False, "")), [1, 2])
assert_equal(find_matching_positions(
    State(make_test_events(), ALL_TEAMS, ALL_DECADES, True, "")), [0, 1])
assert_equal(find_matching_positions(
    State(make_test_events(), "76ers", ALL_DECADES, False, "")), [])
assert_equal(find_matching_positions(
    State([], ALL_TEAMS, ALL_DECADES, False, "")), [])

assert_equal(count_championships(make_test_events(), "Flyers"), 1)
assert_equal(count_championships(make_test_events(), "Eagles"), 0)
assert_equal(count_championships([], "Phillies"), 0)
assert_equal(count_championships(make_starting_events(), "Eagles"), 5)
assert_equal(count_championships(make_starting_events(), "Phillies"), 2)

assert_equal(count_favorites(make_test_events()), 0)
assert_equal(count_favorites(
    [Event("Test", 2000, "76ers", "Test event.", False, True)]), 1)

assert_equal(is_valid_year("1980"), True)
assert_equal(is_valid_year(" 2025 "), True)
assert_equal(is_valid_year("nineteen eighty"), False)
assert_equal(is_valid_year(""), False)
assert_equal(is_valid_year("12"), False)
assert_equal(is_valid_year("3000"), False)

assert_equal(is_valid_position(make_test_events(), 0), True)
assert_equal(is_valid_position(make_test_events(), 2), True)
assert_equal(is_valid_position(make_test_events(), 3), False)
assert_equal(is_valid_position(make_test_events(), -1), False)

assert_equal(find_insert_position(make_test_events(), 1900), 0)
assert_equal(find_insert_position(make_test_events(), 1980), 2)
assert_equal(find_insert_position(make_test_events(), 2020), 3)
assert_equal(find_insert_position([], 2020), 0)

assert_equal(get_team_color("Eagles"), "darkgreen")
assert_equal(get_team_color("Phillies"), "crimson")
assert_equal(get_team_color(ALL_TEAMS), "black")

assert_equal(describe_filters(make_test_state()),
             "Team: All Teams | Decade: All Decades")
assert_equal(describe_filters(
    State([], "Flyers", "1970s", True, "cup")),
    "Team: Flyers | Decade: 1970s | Championships only | Search: cup")

assert_equal(make_event_label(make_test_events()[0]),
             "1974 - Flyers - (Champions) ")
assert_equal(make_event_label(make_test_events()[2]), "1981 - Eagles - ")
assert_equal(make_event_label(
    Event("Test", 2000, "76ers", "Test event.", False, True)),
    "2000 - 76ers - (Saved) ")

assert_equal(make_starting_state().selected_team, ALL_TEAMS)
assert_equal(len(make_starting_events()), 27)

# make_event_row, make_navigation, and make_message_page build Buttons, so
# they are tested through the routes below instead of by themselves.

# Tests for the routes. Most of them check the State that comes back in
# the Page, since that is what the route is supposed to change.
assert_equal(index(make_test_state()).state, make_test_state())
assert_equal(choose_team(make_test_state()).state, make_test_state())
assert_equal(choose_decade(make_test_state()).state, make_test_state())
assert_equal(about_page(make_test_state()).state, make_test_state())
assert_equal(add_event_page(make_test_state()).state, make_test_state())
assert_equal(championships_page(make_test_state()).state, make_test_state())

assert_equal(set_team(make_test_state(), "Eagles").state,
             State(make_test_events(), "Eagles", ALL_DECADES, False, ""))
assert_equal(set_team(make_test_state(), "Not A Team").state,
             State(make_test_events(), ALL_TEAMS, ALL_DECADES, False, ""))

assert_equal(
    set_filters(make_test_state(), "1980s", True, " tug ").state,
    State(make_test_events(), ALL_TEAMS, "1980s", True, "tug"))
assert_equal(
    set_filters(make_test_state(), "Not A Decade", False, "").state,
    State(make_test_events(), ALL_TEAMS, ALL_DECADES, False, ""))

assert_equal(
    clear_filters(State(make_test_events(), "Flyers", "1970s", True,
                        "cup")).state,
    make_test_state())

assert_equal(NO_EVENTS_MESSAGE in show_events(make_test_state()).content,
             False)
assert_equal(
    NO_EVENTS_MESSAGE in show_events(
        State(make_test_events(), "76ers", ALL_DECADES, False, "")).content,
    True)
# 3 things at the top, 1 "Found" line, 3 events, and 3 things at the bottom
assert_equal(len(show_events(make_test_state()).content), 10)
assert_equal(
    len(show_events(State(make_test_events(), "Eagles", ALL_DECADES,
                          False, "")).content), 8)

assert_equal(event_details(make_test_state(), 1).state, make_test_state())
assert_equal(
    "Sorry, that event does not exist." in
    event_details(make_test_state(), 99).content, True)

assert_equal(
    toggle_favorite(make_test_state(), 0).state.events[0].is_favorite, True)
assert_equal(
    toggle_favorite(toggle_favorite(make_test_state(), 0).state,
                    0).state.events[0].is_favorite, False)
assert_equal(toggle_favorite(make_test_state(), 99).state, make_test_state())

assert_equal(
    NO_FAVORITES_MESSAGE in favorites_page(make_test_state()).content, True)
assert_equal(
    NO_FAVORITES_MESSAGE in favorites_page(
        toggle_favorite(make_test_state(), 2).state).content, False)

assert_equal(
    save_new_event(make_test_state(), "Flyers Beat the Soviets", "1976",
                   "Flyers", "Won 4-1.", False).state.events[1],
    Event("Flyers Beat the Soviets", 1976, "Flyers", "Won 4-1.",
          False, False))
assert_equal(
    len(save_new_event(make_test_state(), "Second Super Bowl Win", "2025",
                       "Eagles", "Beat the Chiefs.",
                       True).state.events), 4)
assert_equal(
    save_new_event(make_test_state(), "", "1976", "Flyers", "Won 4-1.",
                   False).state, make_test_state())
assert_equal(
    save_new_event(make_test_state(), "Bad Year", "abc", "Flyers", "",
                   False).state, make_test_state())
assert_equal(
    save_new_event(make_test_state(), "Bad Team", "1976", "Cowboys", "",
                   False).state, make_test_state())


start_server(make_starting_state())
