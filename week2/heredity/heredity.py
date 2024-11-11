import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # initial probability
    prob = 1

    for p in people:
        # set variables for gene and trait from PROBS
        if p in one_gene:
            gene = PROBS['gene'][1]
            gene_num = 1
        elif p in two_genes:
            gene = PROBS['gene'][2]
            gene_num = 2
        else:
            gene = PROBS['gene'][0]
            gene_num = 0
        
        if p in have_trait:
            trait = PROBS['trait'][gene_num][True]
        else:
            trait = PROBS['trait'][gene_num][False]
        
        # we can assume either no parental information, or both entries are filled, use as first case
        if people[p]['mother'] is None and people[p]['father'] is None:
            prob *= gene * trait
        else:
            # Parents are listed, we check each one to see if they have 0, 1 or 2 genes and apply
            mother = people[p]['mother']
            father = people[p]['father']

            if mother in one_gene:
                mother_prob = 0.5
            elif mother in two_genes:
                mother_prob = 1 - PROBS['mutation']
            else:
                mother_prob = PROBS['mutation']

            if father in one_gene:
                father_prob = 0.5
            elif father in two_genes:
                father_prob = 1 - PROBS['mutation']
            else:
                father_prob = PROBS['mutation']
            
            # check what gene the person has
            if p in one_gene:
                # one parent gave the gene
                mother_gave = mother_prob * (1 - father_prob)
                father_gave = father_prob * (1 - mother_prob)
                prob *= mother_gave + father_gave
            elif p in two_genes:
                # both parents gave the gene
                prob *= mother_prob * father_prob
            else:
                # no parents gave gene
                prob *= (1 - father_prob) * (1 - mother_prob)
            
            # check if person has trait
            prob *= trait
    return prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p
    
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total = sum(probabilities[person]['gene'].values())
        for key in probabilities[person]['gene']:
            prob = probabilities[person]['gene'][key]
            normalized = prob / total
            probabilities[person]['gene'][key] = normalized
        
        total = sum(probabilities[person]['trait'].values())
        for key in probabilities[person]['trait']:
            prob = probabilities[person]['trait'][key]
            normalized = prob / total
            probabilities[person]['trait'][key] = normalized


if __name__ == "__main__":
    main()
