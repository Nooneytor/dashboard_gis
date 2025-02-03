import streamlit as st
from utils.territorial_chat import TerritorialChat

# CSS personalizado para mejorar la experiencia del chat
st.markdown(
    """
    <style>
    .chat-container {
        background-color: #ffffff;
        border: 1px solid #ccc;
        padding: 15px;
        border-radius: 8px;
        max-height: 600px;
        overflow-y: auto;
        margin-bottom: 20px;
    }
    .message {
        margin: 10px 0;
    }
    .user-message {
        text-align: right;
    }
    .assistant-message {
        text-align: left;
    }
    .message p {
        display: inline-block;
        padding: 10px;
        border-radius: 10px;
        max-width: 80%;
        margin: 0;
    }
    .user-message p {
        background-color: #d1e7dd;
        color: #0f5132;
    }
    .assistant-message p {
        background-color: #e2e3e5;
        color: #41464b;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar el objeto de chat en st.session_state (si no existe)
if "chat" not in st.session_state:
    st.session_state.chat = TerritorialChat()

st.title("Chat - Desarrollo Territorial")
st.markdown("Utiliza el chat para aportar información complementaria. La respuesta se borrará al enviarla.")

# Contenedor del historial de conversación (se ocultan mensajes de sistema)
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chat.conversation_history:
        # Ocultamos el mensaje del sistema (prompt inicial)
        if msg["role"] == "system":
            continue
        elif msg["role"] == "user":
            st.markdown(
                f'<div class="message user-message"><p><strong>Tú:</strong> {msg["content"]}</p></div>',
                unsafe_allow_html=True,
            )
        elif msg["role"] == "assistant":
            st.markdown(
                f'<div class="message assistant-message"><p><strong>Asistente:</strong> {msg["content"]}</p></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# Formulario para enviar la respuesta (clear_on_submit borra el input al enviar)
with st.form(key="chat_input_form", clear_on_submit=True):
    user_message = st.text_input("Escribe tu respuesta:")
    submitted = st.form_submit_button("Enviar")

if submitted and user_message:
    # Si el nombre aún no ha sido registrado, se asume que es la respuesta al nombre.
    if st.session_state.chat.user_name is None:
        st.session_state.chat.add_user_answer(user_message)
    else:
        st.session_state.chat.add_user_answer(user_message)
        # Control de seguimiento: si se alcanzó el máximo de follow-up, avanzar a la siguiente pregunta obligatoria.
        if st.session_state.chat.follow_up_count >= st.session_state.chat.MAX_FOLLOW_UP:
            st.session_state.chat.go_to_next_mandatory_question()
        else:
            st.session_state.chat.follow_up_count += 1
        # Se solicita la respuesta del modelo y se añade al historial.
        st.session_state.chat.get_model_response()
    st.experimental_rerun()
