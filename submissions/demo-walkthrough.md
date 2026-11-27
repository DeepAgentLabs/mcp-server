# Record the public submission demo

Status: no recording exists yet. This document is a walkthrough, not evidence
that a demo was recorded or that the review cases passed.

Use the working development connection already tested in ChatGPT or Claude.
For the combined plugin, also show the installed four-skill bundle in a host
that supports it; a custom MCP URL alone does not install the skills.

1. Start the screen recorder on a clean dedicated test account. Keep API keys,
   tokens, unrelated chats, account menus and personal data out of the recording.
2. Show the DeepAgentLabs name/icon and connected state. Show the four installed
   skills if demonstrating the bundle, not just the remote connector.
3. In a new conversation, run positive case 1 from `review-cases.json`: hosted
   version/compatibility. Let the viewer read the actual result and the explicit
   separation from local package installation.
4. Run case 2, the seven-product reference catalog. Show the product/version list.
5. Run case 3, the documented AgenticLens example. Show the actual documentation
   tool calls, section retrieval and cited example, without changing a real project.
6. Run case 4, the fault catalog. Show supported suggestions and no execution.
7. Run case 5 with the inline workflow JSON. Show the schema/conformance result
   and preserve its draft status.
8. Run negative cases 1–3. Show that no local script executes, another account's
   records are not exposed, and no local deployment/control is fabricated.
9. Stop recording. Play the saved video back and verify readable text/results,
   actual success/fallback behavior, all required cases and no exposed secrets.
10. Host the recording where reviewers can play it without private permissions,
    using a destination chosen by the publisher. Verify playback before adding
    its URL to the manifest. A private/local video or script is not a completed URL.

Computer control/recording is not available through the connected tools in this
session. The publisher can perform this same walkthrough with their screen
recorder; screenshots or mockups are not substitutes for the required video.
