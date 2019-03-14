export default {

  // validate perms
  validatePermission (permission, userPermissions) {
    let permissionState = false
    for (let i = 0; i < userPermissions.length; i++) {
      let currentPermission = userPermissions[i]
      if (currentPermission === permission) {
        permissionState = true
        break
      } else {
        permissionState = false
      }
    }
    return permissionState
  }

}
