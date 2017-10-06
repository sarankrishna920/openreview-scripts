# create admin user
    create_admin = raw_input("Create administrator login? (y/[n]): ").lower()
    if create_admin == 'y' or create_admin == 'yes':
        default_username = conference_group_id.split('/')[-1].lower()+'_admin'
        username = raw_input("Please provide administrator login, in lowercase, with no spaces (default: {0}): ".format(default_username))
        if not username.strip(): username = default_username
        firstname = raw_input("Please provide administrator first name: ")
        lastname = raw_input("Please provide administrator last name: ")

        passwords_match = False
        while not passwords_match:
            password = getpass.getpass("Please provide a new administrator password: ")
            passwordconfirm = getpass.getpass("Please confirm the new password: ")

            passwords_match = password == passwordconfirm
            if not passwords_match:
                print "Passwords do not match."

        client.register_user(email = username, password=password,first=firstname,last=lastname)

        admin_activated = False
        while not admin_activated:
            manual_activation = raw_input("Would you like to enter the activation token now? (y/[n]): ")
            manual_activation = manual_activation.lower() == 'y'

            if manual_activation:
                try:
                    token = raw_input("Please provide the confirmation token: ")
                    activation = client.activate_user(token = token)
                    print "Admin account activated."
                    print "UserID: ", activation['user']['profile']['id']
                    print "Login: ", username
                    admin_activated = True
                except:
                    print "Invalid token."
            else:
                print "Admin account not activated. Please respond to the email confirmation sent to %s" % username
                admin_activated = True
        client.add_members_to_group(admin_group, [username])
        print "Added %s to %s" % (username, args.conf)
