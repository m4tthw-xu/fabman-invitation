import tiw_secrets
import fabman

secrets = tiw_secrets.Secrets()

fab = fabman.Fabman(secrets.fabman_api_key)

search_term = "Jonathan Bennikutty"
members = fab.get_members(q=search_term)

# Print all matching members
for member in members:
    print(type(member))

    # how to get necessary fields
    print(member)
    print(member.get_invitation())
    print(member.__getattribute__("id"))

    member_id = member.__getattribute__("id")
    
    try:
        response = member._requester.request(
            "POST",
            f"/members/{member_id}/invitation",
            _kwargs={},
        )
        print(f"Invitation sent successfully to member {member_id}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error sending invitation: {e}")


    






