# Assignment3

# Jordan Rinne
# jrinne@uci.edu
# 16935997

This assignment has all the same Profile functionality that assignment 2 had (editing, printing, deleting, opening, creating profiles). Additionally, this program has the option to publish a profile to a local DSP server. You can publish your profile's posts, bio, or both. The publish (PB) function works with both admin and main ui mode. Specifically, the publish function supports sending just the bio (-bio), a single post (-post <index>), all posts (-post -all), the bio and a post (-both <index>), or the bio and all posts (-both -all). The code also detects any errors related to publishing in ui mode (if the server can't be found, index out of bounds, etc.).