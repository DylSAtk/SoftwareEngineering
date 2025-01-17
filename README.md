# SoftwareEngineering
This repo is going to be a better version of my private university repo. Should be more reflective of real world repositories, and the information put in them

# Project Introduction

I wanted to build this project because at our company we record care notes, but we don't perform any meaningful data science. By tracking positive and negative care notes, we can gather an insight into the welfare of the resident. 

# Project Requirements

## UI
- Has to include a way to view a resident's care notes
- Has to include a way to see positive / nuetral / negative care notes
- Has to show all residents in a locaiton

## Resident Data and Care Note Data
- Has to include a list of residents in a database that can be read from and written to
- Has to include a list of care notes in a database that can be read from and written to
- Has to consider the care note semantic analysis

## Semantic Analysis
- Use the care note text and semantic analysis to categorise the care note into a positive neutral or negative category

# User Story

## Persona

### Name:
Jane Smith
### Role:
Care Worker at Fake Care Home
### Goals:
To ensure residents receive accurate and timely care, and to efficiently document and review care-related information

# User Tasks And Goals:

## Log a care note for a resident
Jane navigates to the Add Care Note tab. She searches for the resident by ID
She enters the care note details and hits add care notes

## Check the Number of Positive v Negative Care Notes
Jane navigates to the View Care Notes tab and selects a resident id.
The application then displays the number of positive, neutral and negative care notes and their related percentages
The application should also display the care note text

## Log a new resident
Jane navigates to the Add a New Resident tab and inputs resident info
She selects add new resident
The UI should make it obvious it has worked
If she goes to the view residents tab the new resident should be visible

## View All Reisdents
Jane navigates to the View Residents tab
She should be able to see all the residents and some information about them

## Project Stakeholders
| Role    | Responsibility | Notes |
| -------- | ------- | ------- |
| Project Manager  | In charge of the product    |    |
| Developer | Develops the application     | This could be split into front end back end, but as it's just me, this is all me  |
| Care Worker    | Represents the end user   | Would be the one using the system at the end |

## Project Risks

| **Risk**                                      | **Likelihood** | **Impact** | **Risk Level** (Priority) | **Mitigation Strategy**                                                |
|-----------------------------------------------|----------------|------------|--------------------------|------------------------------------------------------------------------|
| **Database doesn't write back**        | Medium         | High       | Critical                  | - Learn how to program a SQLAlchemy DB, and connect it to a wider program          |
| **Short Project Timeline causing errors/bugs**| High           | Medium     | Medium                    | - Work on this as much as possible|
|                                               |                |            |                          | - Use test driven development and comprehensive testing to mitigate risk of bugs                   |

# Project Management

## Tooling

To organise the tasks, I used the milestone feature in GitHub to assign sprints. This is the closest I could get to my actual workplace style of work, because Sprints are not native to Git. I allocate 3 sprints (week 1, 2, 3) and assigned tickets to those weeks. Each week was allocated a finish point, one week after the other. As a result, this would help me maintain a clear goal for each week.

## Constraints

A lot of this project was definitely under-developed due to a lack of time. I also didn't help myself by choosing 2 development ideas that I haven't done before - building a React product, and hooking a locally hosted Database into a python program. As a result, I had to completely remove the React element idea - which is something I really wanted to implement, but would have taken too long, and replace it with a simpler Streamlit app. However, I did make good progress using SQLAlchemy and a locally hosted DB

## Ticket Templates

To save myself time and to ensure consistency, I designed 3 ticket templates. One was for bugs, one was for features and one was more generic. By doing this, it helped reduce development time by ensuring I had all the information I needed to include in the tickets, and made them quicker to develop, and read.

# Project Planning

## Figma

I designed my product in Figma - it is available at: https://www.figma.com/design/PfYp4oUejZIfacQ435b196/Care-Home-Resident-Interactor?node-id=0-1&t=RimE4RxbQyHBbP6d-1

## Implementation Issues

As mentioned before, I wanted to use React to build this, because it's popular and I thought it would be a good industrious desicision - however I ran out of time so I had to use Streamlit.

# Project Development

## Development Overview

Once the issues were properly backlogged, I started working on developing the application

## Project Timeline

1. **Infrastructure** - I needed the DB to work, have a correct schema and to populate properly. I also needed the data to be retrievable.
2. **UI** - I needed the application to load, so users could enter data
3. **Communication** - The next part was getting the infrastructure to work with the UI
4. **DB Testing** - I needed to build unit tests to check against the database itself
5. **Semantic Analysis** - I needed to analyse the care note entry text - this would involve updating the database
6. **UI Testing** - I needed to check the UI worked properly
7. **End - To - End Testing** - I needed to ensure that from start to finish the product worked

# Test Driven Development (TTD):

By developing the unit test theories before implementing code, I was able to use TTD in this project. Tests can be found in the testing.ipynb file