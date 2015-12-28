import gather

roles = gather.Roles()

for r in sorted(roles.roles.itervalues(), cmp=lambda x, y: cmp(x.roleId, y.roleId)):
    print r.roleId
    for s in sorted(r.scopes):
        print ' ' * 4 + s
