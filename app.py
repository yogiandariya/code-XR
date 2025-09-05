import streamlit as st
import json
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# --- Pydantic Models for JSON Schema Validation ---
# As per the document, using Pydantic ensures the LLM output is structured correctly.

class Task(BaseModel):
    task_name: str = Field(..., description="A single, clear step for the developer to follow.")
    details: Optional[str] = Field(None, description="Optional further explanation for the step.")

class CodeSnippet(BaseModel):
    language: str = Field(..., description="The programming language (e.g., 'csharp', 'cpp', 'hlsl').")
    code: str = Field(..., description="The ready-to-paste code block.")

class CodeXRResponse(BaseModel):
    query: str
    category: str
    difficulty: str = Field(..., description="Estimated difficulty (e.g., 'Beginner', 'Intermediate', 'Advanced').")
    subtasks: List[Task]
    code_snippet: CodeSnippet
    best_practices: List[str] = Field(..., description="Tips, gotchas, or common pitfalls to be aware of.")
    documentation_link: str = Field(..., description="A link to relevant official documentation.")

# --- Simulated LLM & Web Search Backend ---
# In a real application, this function would call an LLM (like GPT-4o-mini)
# and a web search API. For this demo, we simulate the output for the
# three required scenarios from the document.

def get_simulated_ai_response(query: str) -> dict:
    """
    Simulates a response from the CodeXR backend (LLM + Web Search).
    It checks for keywords from the demo scenarios and returns a
    hardcoded, structured JSON response.
    """
    query_lower = query.lower()

    # Scenario 1: Unity Teleport Locomotion
    if "teleport" in query_lower and "unity" in query_lower:
        return {
            "query": query,
            "category": "Unity",
            "difficulty": "Intermediate",
            "subtasks": [
                {"task_name": "Install the Unity XR Interaction Toolkit", "details": "Use the Package Manager to add the XR Interaction Toolkit."},
                {"task_name": "Create a Teleportation Area", "details": "Add a 'Teleportation Area' component to the floor/ground plane."},
                {"task_name": "Set up the XR Rig", "details": "Ensure your XR Rig has a 'Teleportation Provider' component."},
                {"task_name": "Configure Controller Actions", "details": "Map a controller button to the 'Teleport' action in the Input Action Asset."}
            ],
            "code_snippet": {
                "language": "csharp",
                "code": (
                    "// Attach this script to your XR Rig to enable teleportation requests.\n"
                    "using UnityEngine;\n"
                    "using UnityEngine.InputSystem;\n"
                    "using UnityEngine.XR.Interaction.Toolkit;\n\n"
                    "public class TeleportController : MonoBehaviour\n"
                    "{\n"
                    "    public InputActionAsset actionAsset;\n"
                    "    public TeleportationProvider provider;\n\n"
                    "    private InputAction _thumbstick;\n"
                    "    private TeleportRequest _request = new TeleportRequest();\n\n"
                    "    void Start()\n"
                    "    {\n"
                    "        // Ensure the provider is assigned in the Inspector\n"
                    "        if (provider == null) provider = GetComponent<TeleportationProvider>();\n\n"
                    "        var activate = actionAsset.FindActionMap(\"XRI RightHand Locomotion\").FindAction(\"Teleport Mode Activate\");\n"
                    "        activate.Enable();\n"
                    "        activate.performed += OnTeleportActivate;\n\n"
                    "        var cancel = actionAsset.FindActionMap(\"XRI RightHand Locomotion\").FindAction(\"Teleport Mode Cancel\");\n"
                    "        cancel.Enable();\n"
                    "        cancel.performed += OnTeleportCancel;\n"
                    "    }\n\n"
                    "    private void OnTeleportActivate(InputAction.CallbackContext context) { /* Logic to show ray */ }\n"
                    "    private void OnTeleportCancel(InputAction.CallbackContext context) { /* Logic to hide ray and teleport */ }\n"
                    "}"
                )
            },
            "best_practices": [
                "Use Teleportation Anchors for specific teleport points, not just large areas.",
                "Ensure your floor/ground objects are on a layer that the XR Ray Interactor can hit.",
                "A 'NullReferenceException' often means the TeleportationProvider is not assigned in the Inspector."
            ],
            "documentation_link": "https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@2.5/manual/locomotion.html"
        }

    # Scenario 2: Unreal Multiplayer VR
    if "multiplayer" in query_lower and "unreal" in query_lower:
        return {
            "query": query,
            "category": "Unreal",
            "difficulty": "Advanced",
            "subtasks": [
                {"task_name": "Enable a Networking Plugin", "details": "Activate 'Online Subsystem' and a specific platform plugin (e.g., 'OnlineSubsystemSteam')."},
                {"task_name": "Replicate VR Pawn and Actors", "details": "Set the 'Replicates' flag to true on your VRPawn and any networked objects."},
                {"task_name": "Replicate Movement", "details": "Use RPCs (Remote Procedure Calls) like 'Server_Move' and 'Multicast_Move' to sync player position."},
                {"task_name": "Set up a Game Session", "details": "Use the Online Session Interface to create, find, and join multiplayer sessions."}
            ],
            "code_snippet": {
                "language": "cpp",
                "code": (
                    "// Example of a replicated function in your character's header file\n"
                    "UCLASS()\n"
                    "class YOURGAME_API AVRCharacter : public ACharacter\n"
                    "{\n"
                    "    GENERATED_BODY()\n\n"
                    "public:\n"
                    "    // This function is called on the server\n"
                    "    UFUNCTION(Server, Reliable, WithValidation)\n"
                    "    void Server_SomeAction();\n\n"
                    "    // This function is called on all clients\n"
                    "    UFUNCTION(NetMulticast, Reliable)\n"
                    "    void Multicast_SomeEffect();\n\n"
                    "    // Must override this for replicated properties\n"
                    "    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;\n\n"
                    "protected:\n"
                    "    // Replicated property\n"
                    "    UPROPERTY(Replicated)\n"
                    "    float Health;\n"
                    "};"
                )
            },
            "best_practices": [
                "Only replicate what's necessary to save bandwidth.",
                "Avoid running complex logic in 'tick' functions for networked actors.",
                "Use 'Replication Conditions' (e.g., COND_OwnerOnly) to control when and to whom properties are sent."
            ],
            "documentation_link": "https://docs.unrealengine.com/5.3/en-US/multiplayer-and-networking-in-unreal-engine/"
        }

    # Scenario 3: Shader for AR Occlusion
    if "shader" in query_lower and "occlusion" in query_lower:
        return {
            "query": query,
            "category": "Shader",
            "difficulty": "Intermediate",
            "subtasks": [
                {"task_name": "Understand Occlusion Shaders", "details": "An occlusion shader makes objects invisible but still hides objects behind them. It doesn't write color, only depth."},
                {"task_name": "Create a New Shader Graph or File", "details": "In Unity or Unreal, create a new shader asset."},
                {"task_name": "Configure the Shader Properties", "details": "Set the 'Render Queue' to be earlier than your normal geometry and disable color/alpha writes."},
                {"task_name": "Apply the Material", "details": "Create a material from the shader and apply it to the geometry that should occlude (e.g., a model of a table)."}
            ],
            "code_snippet": {
                "language": "hlsl",
                "code": (
                    "// A minimal Unity URP shader for occlusion.\n"
                    "Shader \"Unlit/OcclusionShader\"\n"
                    "{\n"
                    "    Properties\n"
                    "    {\n"
                    "    }\n"
                    "    SubShader\n"
                    "    {\n"
                    "        Tags { \"RenderType\"=\"Opaque\" \"Queue\"=\"Geometry-10\" }\n"
                    "        LOD 100\n"
                    "        Pass\n"
                    "        {\n"
                    "            ColorMask 0 // Don't write to any color channels\n"
                    "            ZWrite On   // Write to the depth buffer\n"
                    "        }\n"
                    "    }\n"
                    "}"
                )
            },
            "best_practices": [
                "The key to occlusion is `ColorMask 0`. This prevents the occluder from being visible.",
                "Make sure the occluder geometry matches the real-world object as closely as possible for convincing AR.",
                "This technique works best when the AR platform provides a mesh of the real-world environment."
            ],
            "documentation_link": "https://docs.unity3d.com/Manual/SL-SubShaderTags.html"
        }

    # Default response if no demo scenario is matched
    return {
        "query": query,
        "category": "General",
        "difficulty": "N/A",
        "subtasks": [{"task_name": "Query not recognized", "details": "This demo only supports the three specific scenarios from the project document. Please try one of them."}],
        "code_snippet": {"language": "text", "code": "No code to display."},
        "best_practices": ["Try asking: 'How do I add teleport locomotion in Unity VR?'"],
        "documentation_link": ""
    }


# --- Streamlit UI ---

st.set_page_config(page_title="CodeXR Assistant", layout="wide")

st.title("🤖 CodeXR: AI Coding Assistant for AR/VR Developers")
st.caption("This is a functional demo based on the Phase 1 requirements. Enter one of the three specified queries to see the assistant in action.")

# Input Layer
query = st.text_input(
    "Enter your developer query:",
    placeholder="e.g., How do I set up multiplayer in Unreal VR?"
)

if st.button("✨ Generate Answer"):
    if query:
        with st.spinner("Thinking... Simulating LLM and Web Search..."):
            # Get the structured response from the simulated backend
            response_data = get_simulated_ai_response(query)

            try:
                # Validate the response against the Pydantic model
                validated_response = CodeXRResponse(**response_data)

                # --- Render the Output UI ---
                st.subheader("✅ Subtasks")
                for task in validated_response.subtasks:
                    st.markdown(f"- **{task.task_name}**: {task.details}" if task.details else f"- **{task.task_name}**")

                st.subheader("💻 Code Snippet")
                st.code(validated_response.code_snippet.code, language=validated_response.code_snippet.language)

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("⚠️ Gotchas & Best Practices")
                    for practice in validated_response.best_practices:
                        st.warning(practice)

                with col2:
                    st.subheader("📊 Metadata")
                    st.info(f"**Difficulty:** {validated_response.difficulty}")
                    st.info(f"**Category:** {validated_response.category}")
                    if validated_response.documentation_link:
                        st.markdown(f"**📚 [Official Documentation]({validated_response.documentation_link})**")
                
                with st.expander("Show Raw JSON Output"):
                    st.json(response_data)

            except ValidationError as e:
                st.error("There was an error processing the AI's response. The JSON output did not match the required schema.")
                st.code(str(e))
                st.json(response_data) # Show the invalid data

    else:
        st.warning("Please enter a query.")

