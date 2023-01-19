# This does not include transfers
SUPPORTED_ACTIONS = ['accept', 'cite', 'consume', 'modify', 'produce', 'use', 'work', 'deliverService']
IN_PR_ACTIONS = ['accept', 'cite', 'consume', 'use', 'work']
OUT_PR_ACTIONS = ['modify', 'produce']
IN_OUT_PR_ACTIONS = ['deliverService']
assert set(IN_PR_ACTIONS + OUT_PR_ACTIONS + IN_OUT_PR_ACTIONS) == set(SUPPORTED_ACTIONS)


MAX_DEPTH = 100000000
AGENT_FRAG = """
    fragment agent on Agent {
        id
        name
    }
"""
LOCATION_FRAG = """
    fragment location on SpatialThing {
        id
        alt
        lat
        long
        mappableAddress
        name
        note
    }
"""
QUANTITY_FRAG = """
    fragment quantity on Measure {
      hasNumericalValue
      hasUnit {
        id
        label
        symbol
      }

    }
"""

RESOURCE_FRAG = """
    fragment resource on EconomicResource {
            id
            name
            onhandQuantity {
                ...quantity
            }
            accountingQuantity {
                ...quantity
            }
            primaryAccountable {
                ...agent
            }
            custodian {
                ...agent
            }
          }
"""

ACTION_FRAG = """
    fragment action on Action {
        id
        inputOutput
        label
        onhandEffect
        pairsWith
        resourceEffect
    }
"""
PROCESSSPEC_FRAG = """
    fragment processspecification on ProcessSpecification {
        id
        name
        note
    }
"""
PROCESS_FRAG = """
    fragment process on Process {
        basedOn {
            ...processspecification
        }
        classifiedAs
        deletable
        finished
        hasBeginning
        hasEnd
        id
        name
        nestedIn {
            id
        }
        # Scenario The process with its inputs and outputs is part of the scenario.

        note
        plannedWithin {
            id
        }
        # Plan: The process with its inputs and outputs is part of the plan.

        previous {
            id
        }
    }
"""


EVENT_FRAG = """
    fragment event on Event {
        action {
            ...action
        }
        agreedIn
        # String Reference to an agreement between agents which specifies the rules or policies or calculations which govern this economic event.

        atLocation {
            ...location
        }

        effortQuantity {
            ...quantity
        }
        hasBeginning
        hasEnd
        hasPointInTime
        id
        inputOf {
            ...process
        }
        outputOf {
            ...process
        }
        note
        previous: ProductionFlowItem
        previousEvent {
            id
        }
        provider {
            ...agent
        }
        receiver {
            ...agent
        }

        realizationOf {
            id
        }
        # Agreement This economic event occurs as part of this agreement.

        resourceClassifiedAs
        resourceConformsTo
        resourceInventoriedAs {
            ...resource
        }

        resourceQuantity {
            ...quantity
        }
        toLocation {
            ...location
        }
        toResourceInventoriedAs {
            ...resource
        }
        triggeredBy {
            ...event
        }
    }
"""
# Potentially recursive fragment

PROPINT_FRAG = """
    fragment proposedintent on ProposedIntent {
        id 
        publishedIn {
            id
            name
        }
    
        publishes {
            id
            name
        }
        reciprocal
    }
"""
    
INTENT_FRAG = """
    fragment intent on Intent {
        name
        note
        id
        action {
            ...action
        }
        agreedIn
        atLocation {
            ...location
        }
        availableQuantity {
            ...quantity
        }
        
        # deletable
        due
        effortQuantity {
            ...quantity
        }
        finished
        hasBeginning
        hasEnd
        hasPointInTime

        inputOf {
            ...process
        }
        outputOf {
            ...process
        }
        
        provider {
            ...agent
        }
        receiver {
            ...agent
        }
        
        publishedIn {
            ...proposedintent
        }
        resourceClassifiedAs
        
        # resourceConformsTo: EconomicResource
# The primary resource specification or definition of an existing or potential economic resource. A resource will have only one, as this specifies exactly what the resource is.

        resourceInventoriedAs {
            ...resource
        }
        resourceQuantity {
            ...quantity
        }
    }
"""

PROPOSAL_FRAG = """
    fragment proposal on Proposal {
        created
        eligibleLocation {
            ...location
        }
        hasBeginning
        hasEnd
        id
        name
        note
        primaryIntents {
            ...intent
        }
        publishes {
            ...proposedintent
        }
        reciprocalIntents {
            ...intent
        }
        status
        unitBased
    }

"""