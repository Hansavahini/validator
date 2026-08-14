const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL;

async function handleResponse(response) {
  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error(
      "Invalid response received from server."
    );
  }

  if (!response.ok || data.error) {
    throw new Error(
      data.error || "Request failed."
    );
  }

  return data;
}

export async function validateEDI(ediText) {
  const response = await fetch(
    `${API_BASE_URL}/api/validate/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        edi_text: ediText,
      }),
    }
  );

  return handleResponse(response);
}

export async function convertEDI(ediText) {
  const response = await fetch(
    `${API_BASE_URL}/api/convert/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        edi_text: ediText,
      }),
    }
  );

  return handleResponse(response);
}

export async function downloadMIR(
  mirContent,
  fileName
) {
  const formData = new URLSearchParams();

  formData.append(
    "mir_content",
    mirContent
  );

  formData.append(
    "file_name",
    fileName
  );

  const response = await fetch(
    `${API_BASE_URL}/api/download/`,
    {
      method: "POST",
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to download MIR file."
    );
  }

  return response.blob();
}