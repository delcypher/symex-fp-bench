def generate_toy_library_dependency_code(depAndTargetInfo):
  import svcb
  import svcb.build
  # Unpack the needed information
  assert isinstance(depAndTargetInfo, svcb.build.CMakeDependencyAndTargetInfo)
  info = depAndTargetInfo.dependencyInfo
  targetName = depAndTargetInfo.targetName
  enableTargetCMakeVariable = depAndTargetInfo.enableTargetCMakeVariable
  disabledTargetReasonsCMakeVariable = depAndTargetInfo.disabledTargetReasonsCMakeVariable
  cmakeIndent = depAndTargetInfo.cmakeIndent

  # Emit code that decides whether or not to build the target.
  preGuardCode = """
if (NOT BUILD_TOY_LIBRARY)
{indent}set({enableTargetCMakeVariable} FALSE)
{indent}list(APPEND {disabledTargetReasonsCMakeVariable} "Toy library not available")
endif()
  """.format(indent=cmakeIndent,
             enableTargetCMakeVariable=enableTargetCMakeVariable,
             disabledTargetReasonsCMakeVariable=disabledTargetReasonsCMakeVariable)

  # Emit code to link the target against the necessary libraries
  # and set include paths. This code is emitted inside the guard so
  # it only has an effect if the target is being built.
  inGuardCode = "{indent}target_include_directories({targetName} PRIVATE ${{TOY_LIBRARY_INCLUDES}})\n".format(
    indent=cmakeIndent,
    targetName=targetName)

  inGuardCode += "{indent}target_link_libraries({targetName} PRIVATE ${{TOY_LIBRARY_LIBS}})\n".format(
    indent=cmakeIndent,
    targetName=targetName)

  return (preGuardCode, inGuardCode)

# Register the handler
register_handler('toy_library', generate_toy_library_dependency_code)
