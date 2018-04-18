def project_or_object(project=None, basecamp_object=None, section_name=None):
    """
    The purpose of this function is to provide a Project ID and Object ID given certain kinds of information or to raise
    the appropriate error if the information given isn't enough.

    Given a project object or ID and/or basecamp_object or ID, determines if the ID for both can be found.
    If `project` is an object and `section_name` is given, the ID of the `basecamp_object` can be determined by
    searching the Project object's `dock` list.

    If a `basecamp_object` is given, the Project ID can be found by looking at its "bucket" dictionary.

    If `project` is an int (the Project ID), then `basecamp_object` cannot be None and vice versa. The other variable
    must also be an int or the object.

    :param project:         a Project object or ID. Optional if `basecamp_object` is an Object
    :type project:          basecampy3.endpoints.projects.Project|int

    :param basecamp_object: a Basecamp Object object or ID. Optional if Project is an Object, the BasecampObject to
                                find is a type that appears in a Project's "dock", and `section_name` is specified.
    :type basecamp_object:  basecampy3.endpoints._base.BasecampObject|int

    :param section_name:    the "name" of the section on a project's "dock". Optional if `basecamp_object` is an object
                                or both `project` and `basecamp_object` are IDs
    :type section_name:     str

    :return:                a tuple where the first element is the Project's ID and the second element is the
                                Basecamp Object's ID
    :rtype:                 (int, int)
    """
    if project is None and basecamp_object is None:
        raise ValueError("At least one parameter must be given")
    if project is None:
        project_id = basecamp_object.bucket['id']  # get the Project ID from the Basecamp object
        object_id = int(basecamp_object)
    elif basecamp_object is None:
        if section_name is None:
            raise ValueError("To find an object's ID with only a Project given, you must specify the section's name "
                             "as it appears in the Project's dock. (i.e. todoset, chat, schedule, vault, inbox, "
                             "message_board)")
        for section in project.dock:
            if section['name'] == section_name:
                object_id = section['id']
                break
        else:
            msg = "{project} does not have '{section}' in its dock. Does this project not use {section}?".format(
                project=str(project),
                section=section_name
            )
            ex = AttributeError(msg)
            raise ex
        project_id = int(project)
    else:
        project_id = int(project)
        object_id = int(basecamp_object)

    return project_id, object_id


def normalize_acl(acl):
    """
    Normalize the grant and/or revoke lists we were given. Handle single item, list of items, etc.
    We want to end up with just a list of IDs. Used by Project object to handle modify_access function.

    :param acl: a list of Person objects or just a Person object
    :return: a list of integers representing the IDs of the Person objects in the list given
    """
    try:
        acl = [int(a) for a in acl]  # convert Person objects to list of ID integers
    except TypeError:  # ok maybe we got a single Person instead of a list of them
        acl = [int(acl)]
    return acl
